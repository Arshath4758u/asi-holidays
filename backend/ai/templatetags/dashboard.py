from django import template

register = template.Library()


@register.simple_tag
def dashboard_counts():
    from ai.models import QuoteCheck, ReplyDraft
    from enquiries.models import Enquiry
    from packages.models import Package

    return {
        "new_enquiries": Enquiry.objects.filter(status="new").count(),
        "hot_leads": Enquiry.objects.filter(lead_score="hot").exclude(status__in=["won", "lost"]).count(),
        "packages_live": Package.objects.filter(is_published=True).count(),
        "awaiting_approval": ReplyDraft.objects.filter(status="pending").count(),
        "quotes_to_review": QuoteCheck.objects.filter(status="new").count(),
    }