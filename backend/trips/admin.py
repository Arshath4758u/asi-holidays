from django.contrib import admin

from .models import Room


class _ReadOnly(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False


@admin.register(Room)
class RoomAdmin(_ReadOnly):
    list_display = ("code", "title", "travellers", "created_at")