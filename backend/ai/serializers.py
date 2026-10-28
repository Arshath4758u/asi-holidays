import re

from rest_framework import serializers

from packages.models import Package

from .models import QuoteCheck


class QuoteCheckSerializer(serializers.ModelSerializer):
    package_slug = serializers.SlugField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = QuoteCheck
        fields = ["name", "whatsapp_number", "quote_text", "consent_followup", "package_slug"]
        extra_kwargs = {
            "quote_text": {"min_length": 30, "max_length": 6000},
            "consent_followup": {"required": True},
        }

    def validate_whatsapp_number(self, value):
        digits = re.sub(r"\D", "", value)
        if not 10 <= len(digits) <= 13:
            raise serializers.ValidationError("Enter a valid WhatsApp number.")
        return digits

    def validate_consent_followup(self, value):
        if not value:
            raise serializers.ValidationError("Please agree to be contacted so we can reply.")
        return value

    def create(self, validated_data):
        slug = validated_data.pop("package_slug", "")
        if slug:
            validated_data["package"] = Package.objects.filter(slug=slug, is_published=True).first()
        return super().create(validated_data)