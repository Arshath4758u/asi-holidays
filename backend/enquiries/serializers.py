import re

from rest_framework import serializers

from packages.models import Package

from .models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):
    package_slug = serializers.SlugField(write_only=True, required=False, allow_blank=True)
    website = serializers.CharField(write_only=True, required=False, allow_blank=True)  # honeypot

    class Meta:
        model = Enquiry
        fields = [
            "name", "whatsapp_number", "destination", "departure_date",
            "travellers", "budget", "message", "consent_followup",
            "package_slug", "website",
        ]

    def validate_whatsapp_number(self, value):
        digits = re.sub(r"\D", "", value)
        if not 10 <= len(digits) <= 13:
            raise serializers.ValidationError("Enter a valid WhatsApp number.")
        return digits

    def create(self, validated_data):
        validated_data.pop("website", None)
        slug = validated_data.pop("package_slug", "")
        if slug:
            validated_data["package"] = Package.objects.filter(slug=slug).first()
        return super().create(validated_data)
