import hashlib
import hmac
import json
import logging

import httpx
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from . import client
from .models import ReplyDraft, WhatsAppMessage
from .services import FALLBACK_ASK, SYSTEM_CONCIERGE, _dump, catalogue, run_background

logger = logging.getLogger(__name__)


def configured():
    return bool(settings.WHATSAPP_TOKEN and settings.WHATSAPP_PHONE_NUMBER_ID)


def send_text(to, body):
    """Send a free-form reply. WhatsApp only allows this within 24 hours of the customer's last message."""
    url = f"https://graph.facebook.com/v21.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    r = httpx.post(
        url,
        headers={"Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"},
        json={"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": body}},
        timeout=15,
    )
    r.raise_for_status()


def _valid_signature(request):
    secret = settings.WHATSAPP_APP_SECRET
    if not secret:
        return False  # never accept unsigned webhook calls, in any mode
    expected = "sha256=" + hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(request.headers.get("X-Hub-Signature-256", ""), expected)


def draft_reply(pk):
    msg = WhatsAppMessage.objects.get(pk=pk)
    reply, language = "", ""
    if msg.kind == "text" and msg.text and client.available():
        try:
            data = client.complete_json(SYSTEM_CONCIERGE, f"<catalogue>{_dump(catalogue())}</catalogue>\n<message>{msg.text}</message>")
            reply, language = str(data.get("reply", ""))[:1500], str(data.get("language", ""))[:30]
        except Exception:
            logger.exception("AI concierge failed for message %s", pk)
    reply = reply or FALLBACK_ASK  # voice notes, images and AI failures end up here
    WhatsAppMessage.objects.filter(pk=pk).update(language=language)
    ReplyDraft.objects.create(message=msg, phone=msg.wa_id, language=language or "English", ai_original=reply, body=reply)


@csrf_exempt
def webhook(request):
    if request.method == "GET":  # Meta's one-time verification handshake
        token = settings.WHATSAPP_VERIFY_TOKEN
        if token and request.GET.get("hub.mode") == "subscribe" and request.GET.get("hub.verify_token") == token:
            return HttpResponse(request.GET.get("hub.challenge", ""), content_type="text/plain")
        return HttpResponseForbidden()
    if request.method != "POST":
        return HttpResponse(status=405)
    if not _valid_signature(request):
        return HttpResponseForbidden()
    try:
        payload = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400)
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            names = {c.get("wa_id"): c.get("profile", {}).get("name", "") for c in value.get("contacts", [])}
            for m in value.get("messages", []):
                if not m.get("id"):
                    continue
                kind = m.get("type", "text")
                text = m.get("text", {}).get("body", "") if kind == "text" else ""
                msg, created = WhatsAppMessage.objects.get_or_create(
                    wamid=m["id"],
                    defaults={"wa_id": m.get("from", ""), "name": names.get(m.get("from"), ""), "kind": kind, "text": text[:2000]},
                )
                if created:
                    run_background(draft_reply, msg.pk)
    return HttpResponse("ok")  # always answer fast so Meta does not retry