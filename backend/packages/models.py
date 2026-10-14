from django.db import models


class Package(models.Model):
    class Region(models.TextChoices):
        INDIA = "india", "India"
        INTERNATIONAL = "international", "International"

    class Category(models.TextChoices):
        HOLIDAY = "holiday", "General holiday"
        HONEYMOON = "honeymoon", "Honeymoon"
        FAMILY = "family", "Family"
        GROUP = "group", "Group tour"
        CORPORATE = "corporate", "Corporate travel"
        CUSTOM = "custom", "Customised itinerary"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    region = models.CharField(max_length=15, choices=Region.choices, default=Region.INDIA)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.HOLIDAY, help_text="Trip type")
    destination = models.CharField(max_length=120)
    duration_days = models.PositiveSmallIntegerField()
    price_from = models.DecimalField(max_digits=10, decimal_places=0, help_text="Per person, INR")
    summary = models.TextField(help_text="One-line highlight shown on cards")
    itinerary = models.TextField(blank=True, help_text="Day-wise plan, one day per line")
    inclusions = models.TextField(blank=True, help_text="One item per line")
    exclusions = models.TextField(blank=True, help_text="One item per line")
    image = models.ImageField(upload_to="packages/", blank=True)

    # Filters shown on the Packages page
    suits_vegetarian = models.BooleanField("Vegetarian food available", default=False)
    suits_jain = models.BooleanField("Jain food available", default=False)
    suits_halal = models.BooleanField("Halal food available", default=False)
    suits_kids = models.BooleanField("Good for kids", default=False)
    suits_seniors = models.BooleanField("Good for seniors", default=False)

    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False, help_text="Shown under Popular packages on the home page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title