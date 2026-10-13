from django.contrib import admin

from .models import Package


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "destination", "duration_days", "price_from", "is_published", "is_featured")
    list_editable = ("price_from", "is_published", "is_featured")
    list_filter = ("category", "is_published", "is_featured")
    search_fields = ("title", "destination")
    prepopulated_fields = {"slug": ("title",)}
