from django.db import models


class Package(models.Model):
    class Category(models.TextChoices):
        INDIA = "india", "India holidays"
        INTERNATIONAL = "international", "International tours"
        FAMILY = "family", "Family holidays"
        HONEYMOON = "honeymoon", "Honeymoon packages"
        GROUP = "group", "Group tours"
        CUSTOM = "custom", "Customised itineraries"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    destination = models.CharField(max_length=120)
    duration_days = models.PositiveSmallIntegerField()
    price_from = models.DecimalField(max_digits=10, decimal_places=0, help_text="Per person, INR")
    summary = models.TextField(help_text="Short description shown on cards")
    itinerary = models.TextField(blank=True, help_text="Day-wise plan, one day per line")
    inclusions = models.TextField(blank=True, help_text="One item per line")
    exclusions = models.TextField(blank=True, help_text="One item per line")
    image = models.ImageField(upload_to="packages/", blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title
