from django.contrib import admin

from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "region", "category", "destination", "duration_days", "price_from", "is_published", "is_featured")
    list_editable = ("price_from", "is_published", "is_featured")
    list_filter = ("region", "category", "is_published", "is_featured")
    search_fields = ("title", "destination")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        (None, {"fields": ("title", "slug", "destination", "region", "category", "duration_days", "price_from", "summary", "image")}),
        ("Plan", {"fields": ("itinerary", "inclusions", "exclusions")}),
        ("Filters", {"fields": ("suits_vegetarian", "suits_jain", "suits_halal", "suits_kids", "suits_seniors")}),
        ("Visibility", {"fields": ("is_published", "is_featured")}),
    )