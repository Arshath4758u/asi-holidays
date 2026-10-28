from datetime import date, timedelta

from django.core import mail
from django.test import override_settings
from rest_framework.test import APITestCase

from packages.models import Package

from .models import Enquiry, WhatsAppClick

GOOD = {"name": "Ravi", "whatsapp_number": "98765 43210", "travellers": 2, "consent_followup": True}


@override_settings(ENQUIRY_NOTIFY_EMAILS=["team@example.com"], REST_FRAMEWORK={
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_THROTTLE_RATES": {"enquiry": "1000/hour", "wa_click": "1000/hour"},
})
class EnquiryApiTests(APITestCase):
    def post(self, **extra):
        return self.client.post("/api/enquiries/", {**GOOD, **extra}, format="json")

    def test_create_saves_and_emails_team(self):
        Package.objects.create(title="Goa", slug="goa", destination="Goa", duration_days=3, price_from=1, summary="s", is_published=True)
        r = self.post(package_slug="goa", email="r@example.com", travel_month="December", source="package_form")
        self.assertEqual(r.status_code, 201)
        e = Enquiry.objects.get()
        self.assertEqual(e.whatsapp_number, "9876543210")
        self.assertEqual(e.package.slug, "goa")
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ravi", mail.outbox[0].body)

    def test_consent_required(self):
        r = self.post(consent_followup=False)
        self.assertEqual(r.status_code, 400)
        self.assertIn("consent_followup", r.json())

    def test_consent_missing_entirely_is_rejected(self):
        body = {k: v for k, v in GOOD.items() if k != "consent_followup"}
        r = self.client.post("/api/enquiries/", body, format="json")
        self.assertEqual(r.status_code, 400)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_bad_phone_and_past_date(self):
        self.assertEqual(self.post(whatsapp_number="12").status_code, 400)
        past = (date.today() - timedelta(days=1)).isoformat()
        self.assertEqual(self.post(departure_date=past).status_code, 400)

    def test_honeypot_saves_nothing(self):
        r = self.post(website="http://spam")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Enquiry.objects.count(), 0)

    def test_mail_failure_does_not_lose_lead(self):
        with override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend", EMAIL_HOST="127.0.0.1", EMAIL_PORT=1):
            r = self.post()
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Enquiry.objects.count(), 1)

    def test_whatsapp_click(self):
        r = self.client.post("/api/whatsapp-click/", {"page": "/packages/goa"}, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertEqual(WhatsAppClick.objects.count(), 1)
