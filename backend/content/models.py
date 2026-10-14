from django.db import models


class SiteSettings(models.Model):
    """Single row. Edited by the team in the admin; shown in header, footer, Contact and Thank-you pages."""

    whatsapp_number = models.CharField(max_length=15, blank=True, help_text="Country code + number, digits only, e.g. 919876543210")
    phone_display = models.CharField("Phone (as shown)", max_length=40, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    opening_hours = models.CharField(max_length=120, blank=True)
    response_time = models.CharField(max_length=60, default="2 working hours", help_text="Shown on the Thank-you page")
    about_text = models.TextField(default="ASI Holidays (ASI Global Travel) plans holidays and tours for individuals, families, groups and corporate clients.")
    mission = models.TextField(default="Make holiday planning simple, personal and trustworthy for every traveller.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site settings"


class PolicyPage(models.Model):
    class Slug(models.TextChoices):
        PRIVACY = "privacy", "Privacy policy"
        TERMS = "terms", "Terms and conditions"
        CANCELLATION = "cancellation", "Cancellation and refunds"

    slug = models.CharField(max_length=20, choices=Slug.choices, unique=True)
    body = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    @property
    def title(self):
        return self.get_slug_display()

    def __str__(self):
        return self.title