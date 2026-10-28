import json

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from . import whatsapp
from .models import QuoteCheck, ReplyDraft, WhatsAppMessage, wa_number


@admin.register(ReplyDraft)
class ReplyDraftAdmin(admin.ModelAdmin):
    list_display = ("created_at", "phone", "language", "status", "preview", "open_link")
    list_filter = ("status", "language")
    readonly_fields = ("ai_original", "created_at", "approved_at", "enquiry", "message", "open_link")
    actions = ["approve_and_send", "approve_only", "mark_sent", "reject"]

    @admin.display(description="Draft")
    def preview(self, obj):
        return obj.body[:80]

    @admin.display(description="Send")
    def open_link(self, obj):
        if obj.pk and obj.status != ReplyDraft.Status.REJECTED:
            return format_html('<a href="{}" target="_blank" rel="noopener">Open in WhatsApp</a>', obj.whatsapp_url)
        return "-"

    @admin.action(description="Approve and send via WhatsApp Cloud API")
    def approve_and_send(self, request, queryset):
        for d in queryset.exclude(status__in=[ReplyDraft.Status.SENT, ReplyDraft.Status.REJECTED]):
            if not whatsapp.configured():
                d.status, d.approved_at = ReplyDraft.Status.APPROVED, timezone.now()
                d.save(update_fields=["status", "approved_at"])
                self.message_user(request, "WhatsApp Cloud API is not set up, so drafts were only approved. Use the Open in WhatsApp link to send.", level="warning")
                return
            try:
                whatsapp.send_text(wa_number(d.phone), d.body)
            except Exception as exc:
                self.message_user(request, f"Could not send to {d.phone}: {exc}", level="error")
                continue
            d.status, d.approved_at = ReplyDraft.Status.SENT, timezone.now()
            d.save(update_fields=["status", "approved_at"])
        self.message_user(request, "Done.")

    @admin.action(description="Approve (send manually with the link)")
    def approve_only(self, request, queryset):
        queryset.filter(status=ReplyDraft.Status.PENDING).update(status=ReplyDraft.Status.APPROVED, approved_at=timezone.now())

    @admin.action(description="Mark as sent")
    def mark_sent(self, request, queryset):
        queryset.exclude(status=ReplyDraft.Status.REJECTED).update(status=ReplyDraft.Status.SENT)

    @admin.action(description="Reject")
    def reject(self, request, queryset):
        queryset.update(status=ReplyDraft.Status.REJECTED)


@admin.register(QuoteCheck)
class QuoteCheckAdmin(admin.ModelAdmin):
    list_display = ("created_at", "name", "whatsapp_number", "package", "status")
    list_filter = ("status",)
    list_editable = ("status",)
    readonly_fields = ("name", "whatsapp_number", "package", "quote_text", "analysis", "ai_comparison", "created_at", "send_link")
    fields = ("name", "whatsapp_number", "package", "quote_text", "analysis", "ai_comparison", "consultant_note", "send_link", "status", "created_at")

    @admin.display(description="AI extraction (internal)")
    def analysis(self, obj):
        return format_html("<pre style='white-space:pre-wrap'>{}</pre>", json.dumps(obj.ai_analysis, indent=2, ensure_ascii=False)) if obj.ai_analysis else "-"

    @admin.display(description="Send reply")
    def send_link(self, obj):
        if obj.pk and obj.consultant_note:
            return format_html('<a href="{}" target="_blank" rel="noopener">Open in WhatsApp</a>', obj.whatsapp_url)
        return "Write your reply above, save, then the link appears."


@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ("received_at", "wa_id", "name", "kind", "language", "text")
    readonly_fields = [f.name for f in WhatsAppMessage._meta.fields]

    def has_add_permission(self, request):
        return False