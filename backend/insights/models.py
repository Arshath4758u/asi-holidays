from django.db import models


class InsightReport(models.Model):
    period_start = models.DateField()
    period_end = models.DateField()
    stats = models.JSONField(default=dict)
    summary = models.TextField(blank=True)
    emailed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-period_end"]
        constraints = [models.UniqueConstraint(fields=["period_start", "period_end"], name="one_report_per_period")]

    def __str__(self):
        return f"Insights {self.period_start} to {self.period_end}"