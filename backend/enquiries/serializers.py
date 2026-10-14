import re
from datetime import date

from rest_framework import serializers

from packages.models import Package

from .models import Enquiry


class EnquirySerializer(serializers.ModelSerializer):
    package_slug = serializers.SlugField(write_only=True, required=False, allow_blank=True)
    source = serializers.ChoiceField(choices=["package_form", "contact_form"], required=False)

    class Meta:
        model = Enquiry
        fields = [
            "name", "whatsapp_number", "email", "destination", "departure_date", "travel_month",
            "travellers", "budget", "message", "consent_followup", "source", "package_slug",
        ]
        extra_kwargs = {
            "travellers": {"min_value": 1, "max_value": 200},
            "consent_followup": {"required": True},  # omitted field must fail, not default to False
        }

    def validate_whatsapp_number(self, value):
        digits = re.sub(r"\D", "", value)
        if not 10 <= len(digits) <= 13:
            raise serializers.ValidationError("Enter a valid WhatsApp number.")
        return digits

    def validate_departure_date(self, value):
        if value and value < date.today():
            raise serializers.ValidationError("Travel date cannot be in the past.")
        return value

    def validate_consent_followup(self, value):
        if not value:
            raise serializers.ValidationError("Please agree to be contacted so we can reply.")
        return value

    def create(self, validated_data):
        slug = validated_data.pop("package_slug", "")
        if slug:
            validated_data["package"] = Package.objects.filter(slug=slug).first()
        return super().create(validated_data)