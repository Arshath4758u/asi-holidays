from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .serializers import QuoteCheckSerializer
from .services import analyse_quote, notify_quote, plan_trip, run_background


class PlanView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "ai"

    def post(self, request):
        query = str(request.data.get("query", "")).strip()
        if not 3 <= len(query) <= 300:
            return Response({"query": ["Describe your trip in a few words (3 to 300 characters)."]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(plan_trip(query, request))


class QuoteCheckView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "quote_check"

    def post(self, request):
        if request.data.get("website"):  # honeypot
            return Response({"ok": True}, status=status.HTTP_201_CREATED)
        serializer = QuoteCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        q = serializer.save()
        notify_quote(q)
        run_background(analyse_quote, q.pk)
        return Response({"ok": True}, status=status.HTTP_201_CREATED)