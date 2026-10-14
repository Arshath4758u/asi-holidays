from django.contrib import admin
from django.utils.html import format_html

from .models import Enquiry, WhatsAppClick


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "chat", "destination", "travel", "travellers", "budget", "status", "lead_score", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "lead_score", "package", "source")
    search_fields = ("name", "whatsapp_number", "email", "destination")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
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