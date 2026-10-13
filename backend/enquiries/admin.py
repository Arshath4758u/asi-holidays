from django.contrib import admin

from .models import Enquiry, WhatsAppClick


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "whatsapp_number", "destination", "departure_date", "travellers", "budget", "status", "lead_score", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "lead_score", "package")
    search_fields = ("name", "whatsapp_number", "destination")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)


@admin.register(WhatsAppClick)
class WhatsAppClickAdmin(admin.ModelAdmin):
    list_display = ("created_at", "package", "page")
    list_filter = ("package",)
