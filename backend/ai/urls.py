from django.urls import path

from .search import SearchView
from .views import PlanView, QuoteCheckView
from .whatsapp import webhook

urlpatterns = [
    path("ai/plan/", PlanView.as_view()),
    path("ai/quote-check/", QuoteCheckView.as_view()),
    path("search/", SearchView.as_view()),
    path("whatsapp/webhook/", webhook),
]