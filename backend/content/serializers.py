from rest_framework import serializers

from .models import PolicyPage, SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        exclude = ["id"]


class PolicyPageSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)

    class Meta:
        model = PolicyPage
        fields = ["slug", "title", "body"]