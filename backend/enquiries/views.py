from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from packages.models import Package

from .models import WhatsAppClick
from .notifications import notify_team
from .serializers import EnquirySerializer


class EnquiryCreateView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "enquiry"

    def post(self, request):
        # Honeypot: bots fill hidden fields. Pretend success, save nothing.
        if request.data.get("website"):
            return Response({"ok": True}, status=status.HTTP_201_CREATED)
        serializer = EnquirySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enquiry = serializer.save()
        notify_team(enquiry)
        return Response({"ok": True, "name": enquiry.name}, status=status.HTTP_201_CREATED)


class WhatsAppClickView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "wa_click"

    def post(self, request):
        slug = request.data.get("package_slug", "")
        package = Package.objects.filter(slug=slug).first() if slug else None
        WhatsAppClick.objects.create(package=package, page=str(request.data.get("page", ""))[:200])
        return Response({"ok": True}, status=status.HTTP_201_CREATED)