from rest_framework import serializers

from .models import Package


def _lines(text):
    return [line.strip() for line in text.splitlines() if line.strip()]


class PackageListSerializer(serializers.ModelSerializer):
    region_label = serializers.CharField(source="get_region_display", read_only=True)
    category_label = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Package
        fields = [
            "id", "title", "slug", "region", "region_label", "category", "category_label",
            "destination", "duration_days", "price_from", "summary", "image", "is_featured",
            "suits_vegetarian", "suits_jain", "suits_halal", "suits_kids", "suits_seniors",
        ]


class PackageDetailSerializer(PackageListSerializer):
    itinerary = serializers.SerializerMethodField()
    inclusions = serializers.SerializerMethodField()
    exclusions = serializers.SerializerMethodField()

    class Meta(PackageListSerializer.Meta):
        fields = PackageListSerializer.Meta.fields + ["itinerary", "inclusions", "exclusions"]

    def get_itinerary(self, obj):
        return _lines(obj.itinerary)

    def get_inclusions(self, obj):
        return _lines(obj.inclusions)

    def get_exclusions(self, obj):
        return _lines(obj.exclusions)
