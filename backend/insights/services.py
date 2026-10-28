import json
import logging
from collections import Counter
from datetime import date, datetime, time, timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count
from django.utils import timezone

from ai import client
from ai.models import QuoteCheck, ReplyDraft
from enquiries.models import Enquiry, WhatsAppClick

from .models import InsightReport

logger = logging.getLogger(__name__)

SYSTEM_INSIGHTS = (
    "You write a short weekly briefing for the owner of ASI Holidays, a travel agency. The owner is not technical. "
    "Use only the numbers inside <stats>. Never invent a figure. Plain text, no markdown symbols. Format: a one-line headline, "
    "then 'What went well' (up to 2 lines), 'What needs attention' (up to 3 lines; mention unanswered enquiries and quotes not followed up if the numbers show them), "
    "then 'Do this week' (up to 3 concrete actions). Under 170 words."
)


def _bounds(start, end):
    tz = timezone.get_current_timezone()
    return (timezone.make_aware(datetime.combine(start, time.min), tz),
            timezone.make_aware(datetime.combine(end + timedelta(days=1), time.min), tz))


def compute_stats(start, end):
    """Aggregates only. No names, phone numbers or messages."""
    lo, hi = _bounds(start, end)
    days = (end - start).days + 1
    enq = Enquiry.objects.filter(created_at__gte=lo, created_at__lt=hi)
    prev_total = Enquiry.objects.filter(created_at__gte=lo - timedelta(days=days), created_at__lt=lo).count()
    total = enq.count()
    status = dict(enq.values_list("status").annotate(n=Count("id")))

    labels = [((e.package.title if e.package_id else e.destination.strip().title()) or "Not specified")[:60] for e in enq.select_related("package")]
    clicks = (WhatsAppClick.objects.filter(created_at__gte=lo, created_at__lt=hi)
              .values("package__title").annotate(n=Count("id")).order_by("-n")[:5])

    return {
        "period": {"start": str(start), "end": str(end), "days": days},
        "enquiries": {"total": total, "previous_period": prev_total},
        "lead_score": {k: enq.filter(lead_score=k).count() for k in ("hot", "warm", "cold")},
        "funnel": {k: status.get(k, 0) for k in ("new", "contacted", "quoted", "won", "lost")},
        "booked_percent": round(100 * status.get("won", 0) / total) if total else 0,
        "unanswered_over_2_days": enq.filter(status="new", created_at__lt=timezone.now() - timedelta(days=2)).count(),
        "top_interests": [{"name": n, "enquiries": c} for n, c in Counter(labels).most_common(5)],
        "whatsapp_clicks_total": WhatsAppClick.objects.filter(created_at__gte=lo, created_at__lt=hi).count(),
        "whatsapp_clicks_top": [{"name": r["package__title"] or "General (no package)", "clicks": r["n"]} for r in clicks],
        "languages": [{"name": n, "enquiries": c} for n, c in Counter(e.language for e in enq if e.language).most_common(3)],
        "quote_checks": {"received": QuoteCheck.objects.filter(created_at__gte=lo, created_at__lt=hi).count(),
                         "waiting_for_review": QuoteCheck.objects.filter(status="new").count()},
        "reply_drafts_waiting_approval": ReplyDraft.objects.filter(status="pending").count(),
    }


def fallback_summary(s):
    e, f = s["enquiries"], s["funnel"]
    change = e["total"] - e["previous_period"]
    trend = "up" if change > 0 else "down" if change < 0 else "unchanged"
    lines = [f"{e['total']} enquiries in the last {s['period']['days']} days ({trend} {abs(change)} on the week before)."]
    if s["top_interests"]:
        lines.append("Most asked about: " + ", ".join(f"{t['name']} ({t['enquiries']})" for t in s["top_interests"][:3]) + ".")
    lines.append(f"Hot leads: {s['lead_score']['hot']}. Booked: {f['won']} ({s['booked_percent']}%). Quotes sent but not booked: {f['quoted']}.")
    if s["unanswered_over_2_days"]:
        lines.append(f"Needs attention: {s['unanswered_over_2_days']} enquiries have had no response for over 2 days.")
    if s["reply_drafts_waiting_approval"]:
        lines.append(f"{s['reply_drafts_waiting_approval']} reply drafts are waiting for approval.")
    if s["quote_checks"]["waiting_for_review"]:
        lines.append(f"{s['quote_checks']['waiting_for_review']} quote checks are waiting for a consultant.")
    return "\n".join(lines)


def write_summary(stats):
    if client.available():
        try:
            return client.complete(SYSTEM_INSIGHTS, f"<stats>{json.dumps(stats, ensure_ascii=False)}</stats>", max_tokens=600).strip()
        except Exception:
            logger.exception("AI insights summary failed")
    return fallback_summary(stats)


def build_report(days=7, today=None):
    """Report for the last `days` full days, ending yesterday."""
    end = (today or date.today()) - timedelta(days=1)
    start = end - timedelta(days=days - 1)
    stats = compute_stats(start, end)
    report, _ = InsightReport.objects.update_or_create(
        period_start=start, period_end=end, defaults={"stats": stats, "summary": write_summary(stats)})
    return report


def email_report(report):
    if not settings.ENQUIRY_NOTIFY_EMAILS:
        return False
    try:
        send_mail(f"ASI Holidays weekly insights: {report.period_start} to {report.period_end}", report.summary,
                  settings.DEFAULT_FROM_EMAIL, settings.ENQUIRY_NOTIFY_EMAILS)
    except Exception:
        logger.exception("Could not email insights report")
        return False
    report.emailed = True
    report.save(update_fields=["emailed"])
    return True