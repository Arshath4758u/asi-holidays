import json

from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import InsightReport
from .services import build_report


@admin.register(InsightReport)
class InsightReportAdmin(admin.ModelAdmin):
    change_list_template = "admin/insights/change_list.html"
    list_display = ("period_start", "period_end", "enquiries", "hot_leads", "emailed")
    fields = ("period_start", "period_end", "summary", "stats_view", "emailed", "created_at")
    readonly_fields = fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Enquiries")
    def enquiries(self, obj):
        return obj.stats.get("enquiries", {}).get("total")

    @admin.display(description="Hot leads")
    def hot_leads(self, obj):
        return obj.stats.get("lead_score", {}).get("hot")

    @admin.display(description="Numbers behind the summary")
    def stats_view(self, obj):
        return format_html("<pre style='white-space:pre-wrap'>{}</pre>", json.dumps(obj.stats, indent=2, ensure_ascii=False))

    def get_urls(self):
        return [path("generate/", self.admin_site.admin_view(self.generate), name="insights_generate")] + super().get_urls()

    def generate(self, request):
        if not self.has_view_permission(request):
            self.message_user(request, "No permission.", messages.ERROR)
            return redirect("admin:index")
        report = build_report(7)
        self.message_user(request, "Report generated for the last 7 days.")
        return redirect(reverse("admin:insights_insightreport_change", args=[report.pk]))