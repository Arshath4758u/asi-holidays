from rest_framework.test import APITestCase


class ContentApiTests(APITestCase):
    def test_site_settings_available_with_defaults(self):
        r = self.client.get("/api/site/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("whatsapp_number", r.json())
        self.assertIn("response_time", r.json())

    def test_three_policies_seeded(self):
        r = self.client.get("/api/policies/")
        self.assertEqual({p["slug"] for p in r.json()}, {"privacy", "terms", "cancellation"})
