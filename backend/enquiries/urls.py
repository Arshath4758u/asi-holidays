from django.urls import path

from .views import EnquiryCreateView, WhatsAppClickView

urlpatterns = [
    path("enquiries/", EnquiryCreateView.as_view()),
    path("whatsapp-click/", WhatsAppClickView.as_view()),
]
