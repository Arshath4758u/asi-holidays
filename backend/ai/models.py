from urllib.parse import quote

from django.db import models

from enquiries.models import Enquiry
from packages.models import Package


def wa_number(raw):
    digits = "".join(c for c in raw if c.isdigit())
    return "91" + digits if len(digits) == 10 else digits  # Indian number without country code


class WhatsAppMessage(models.Model):
    """Inbound message received by the WhatsApp concierge webhook."""

    wamid = models.CharField(max_length=128, unique=True)
    wa_id = models.CharField("Customer number", max_length=20)
    name = models.CharField(max_length=120, blank=True)
    kind = models.CharField(max_length=20, default="text")
    text = models.TextField(blank=True)
    language = models.CharField(max_length=30, blank=True)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-received_at"]

    def __str__(self):
        return f"{self.wa_id}: {self.text[:40]}"


class ReplyDraft(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Awaiting approval"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        SENT = "sent", "Sent"

    enquiry = models.ForeignKey(Enquiry, null=True, blank=True, on_delete=models.SET_NULL, related_name="drafts")
    message = models.ForeignKey(WhatsAppMessage, null=True, blank=True, on_delete=models.SET_NULL, related_name="drafts")
    phone = models.CharField(max_length=20)
    language = models.CharField(max_length=30, blank=True)
    ai_original = models.TextField(blank=True, help_text="What the AI wrote, kept for audit")
    body = models.TextField(help_text="Edit this before approving")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def whatsapp_url(self):
        return f"https://wa.me/{wa_number(self.phone)}?text={quote(self.body)}"

    def __str__(self):
        return f"Draft for {self.phone} ({self.status})"


class QuoteCheck(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        REVIEWED = "reviewed", "Reviewed by consultant"
        SENT = "sent", "Sent to customer"

    name = models.CharField(max_length=120)
    whatsapp_number = models.CharField(max_length=20)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL)
    quote_text = models.TextField()
    consent_followup = models.BooleanField(default=False)
    ai_analysis = models.JSONField(default=dict, blank=True)
    ai_comparison = models.TextField(blank=True, help_text="AI draft for the consultant. Never shown to the customer directly.")
    consultant_note = models.TextField(blank=True, help_text="Write the reply to send to the customer")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def whatsapp_url(self):
        return f"https://wa.me/{wa_number(self.whatsapp_number)}?text={quote(self.consultant_note)}"

    def __str__(self):
        return f"Quote check: {self.name}"