from django.contrib import admin
from django.utils.html import format_html

from ai.models import ReplyDraft

from .models import Enquiry, WhatsAppClick

SCORE_COLOURS = {"hot": "#b3261e", "warm": "#b26a00", "cold": "#4a5a8a"}


class ReplyDraftInline(admin.StackedInline):
    model = ReplyDraft
    extra = 0
    can_delete = False
    fields = ("status", "body", "ai_original", "open_link")
    readonly_fields = ("ai_original", "open_link")

    @admin.display(description="Send")
    def open_link(self, obj):
        if obj.pk and obj.status != ReplyDraft.Status.REJECTED:
            return format_html('<a href="{}" target="_blank" rel="noopener">Open in WhatsApp</a>', obj.whatsapp_url)
        return "-"


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "chat", "destination", "travel", "travellers", "budget", "score", "status", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "lead_score", "package", "source")
    search_fields = ("name", "whatsapp_number", "email", "destination")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "ai_summary", "language")
    inlines = [ReplyDraftInline]
    actions = ["mark_contacted", "mark_quoted", "mark_won", "mark_lost"]

    @admin.display(description="WhatsApp")
    def chat(self, obj):
        number = obj.whatsapp_number
        if len(number) == 10:  # Indian number without country code
            number = "91" + number
        return format_html('<a href="https://wa.me/{}" target="_blank" rel="noopener">{}</a>', number, obj.whatsapp_number)

    @admin.display(description="Travel")
    def travel(self, obj):
        return obj.departure_date or obj.travel_month or "-"

    @admin.display(description="Lead", ordering="lead_score")
    def score(self, obj):
        if not obj.lead_score:
            return "-"
        return format_html('<b style="color:{}">{}</b>', SCORE_COLOURS.get(obj.lead_score, "#000"), obj.get_lead_score_display())

    def _set(self, request, queryset, status, label):
        n = queryset.update(status=status)
        self.message_user(request, f"{n} enquiries marked {label}.")

    @admin.action(description="Mark as contacted")
    def mark_contacted(self, request, queryset):
        self._set(request, queryset, Enquiry.Status.CONTACTED, "contacted")

    @admin.action(description="Mark as quote sent")
    def mark_quoted(self, request, queryset):
        self._set(request, queryset, Enquiry.Status.QUOTED, "quote sent")

    @admin.action(description="Mark as booked")
    def mark_won(self, request, queryset):
        self._set(request, queryset, Enquiry.Status.WON, "booked")

    @admin.action(description="Mark as lost")
    def mark_lost(self, request, queryset):
        self._set(request, queryset, Enquiry.Status.LOST, "lost")


@admin.register(WhatsAppClick)
class WhatsAppClickAdmin(admin.ModelAdmin):
    list_display = ("created_at", "package", "page")
    list_filter = ("package",)