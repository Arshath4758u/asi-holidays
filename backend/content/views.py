from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PolicyPage, SiteSettings
from .serializers import PolicyPageSerializer, SiteSettingsSerializer


class SiteSettingsView(APIView):
    def get(self, request):
        return Response(SiteSettingsSerializer(SiteSettings.load()).data)


class PolicyListView(APIView):
    def get(self, request):
        return Response(PolicyPageSerializer(PolicyPage.objects.all(), many=True).data)
