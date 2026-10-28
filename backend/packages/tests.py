from rest_framework.test import APITestCase

from .models import Package


def make(slug, **kw):
    base = dict(title=slug, slug=slug, destination="X", duration_days=3, price_from=1000, summary="s", is_published=True)
    base.update(kw)
    return Package.objects.create(**base)


class PackageApiTests(APITestCase):
    def setUp(self):
        make("kerala", region="india", category="family", suits_vegetarian=True, suits_jain=True, suits_kids=True, itinerary="Day 1: A\nDay 2: B")
        make("dubai", region="international", category="holiday", suits_halal=True)
        make("kashmir", region="india", category="honeymoon", suits_vegetarian=True)
        make("hidden", is_published=False)

    def slugs(self, qs=""):
        r = self.client.get(f"/api/packages/{qs}")
        self.assertEqual(r.status_code, 200)
        return {p["slug"] for p in r.json()}

    def test_only_published(self):
        self.assertEqual(self.slugs(), {"kerala", "dubai", "kashmir"})

    def test_region_filter(self):
        self.assertEqual(self.slugs("?region=international"), {"dubai"})
        self.assertEqual(self.slugs("?region=india,international"), {"kerala", "dubai", "kashmir"})

    def test_trip_type_filter(self):
        self.assertEqual(self.slugs("?category=honeymoon,family"), {"kerala", "kashmir"})

    def test_food_filter_requires_all(self):
        self.assertEqual(self.slugs("?food=veg"), {"kerala", "kashmir"})
        self.assertEqual(self.slugs("?food=veg,jain"), {"kerala"})
        self.assertEqual(self.slugs("?food=halal"), {"dubai"})

    def test_with_filter(self):
        self.assertEqual(self.slugs("?with=kids"), {"kerala"})

    def test_combined_filters(self):
        self.assertEqual(self.slugs("?region=india&category=family&food=veg&with=kids"), {"kerala"})

    def test_detail_and_unpublished_404(self):
        r = self.client.get("/api/packages/kerala/")
        self.assertEqual(r.json()["itinerary"], ["Day 1: A", "Day 2: B"])
        self.assertEqual(self.client.get("/api/packages/hidden/").status_code, 404)
