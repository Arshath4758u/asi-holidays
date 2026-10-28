from django.db import models

from packages.models import Package


class Enquiry(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUOTED = "quoted", "Quote sent"
        WON = "won", "Booked"
        LOST = "lost", "Lost"

    # Reserved for Phase 2A lead scoring
    class Score(models.TextChoices):
        HOT = "hot", "Hot"
        WARM = "warm", "Warm"
        COLD = "cold", "Cold"

    name = models.CharField(max_length=120)
    whatsapp_number = models.CharField(max_length=20)
    destination = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    departure_date = models.DateField(null=True, blank=True)
    travel_month = models.CharField(max_length=30, blank=True, help_text="e.g. December")
    travellers = models.PositiveSmallIntegerField(default=1)
    budget = models.CharField(max_length=60, blank=True, help_text="Free text, e.g. 50k-70k per person")
    message = models.TextField(blank=True)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name="enquiries")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    lead_score = models.CharField(max_length=4, choices=Score.choices, blank=True)
    follow_up_notes = models.TextField(blank=True, help_text="Record each follow-up here")
    consent_followup = models.BooleanField(default=False)
    source = models.CharField(max_length=20, blank=True, help_text="package_form, contact_form")
    created_at = models.DateTimeField(auto_now_add=True)
    ai_summary = models.TextField(blank=True)
    language = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} - {self.destination or 'general'}"


class WhatsAppClick(models.Model):
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL)
    page = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
