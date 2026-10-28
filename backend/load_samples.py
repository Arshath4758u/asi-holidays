import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from packages.models import Package  # noqa: E402

SAMPLES = [
    dict(slug="sample-kerala-family", title="Kerala Backwaters Family Escape (sample)", destination="Kerala", region="india",
         category="family", duration_days=5, price_from=18000, is_featured=True,
         suits_vegetarian=True, suits_jain=True, suits_kids=True, suits_seniors=True,
         summary="Houseboat stay, hill station and beach in one easy family trip.",
         itinerary="Arrive Kochi, transfer to Munnar\nMunnar tea gardens and sightseeing\nTransfer to Thekkady, spice plantation visit\nAlleppey houseboat stay\nKovalam beach, departure",
         inclusions="Hotel stay\nBreakfast and dinner\nPrivate cab transfers\nSightseeing", exclusions="Flights\nPersonal expenses"),
    dict(slug="sample-kashmir-honeymoon", title="Kashmir Honeymoon Special (sample)", destination="Kashmir", region="india",
         category="honeymoon", duration_days=6, price_from=26000, is_featured=True, suits_vegetarian=True, suits_halal=True,
         summary="Shikara ride, Gulmarg gondola and a Dal Lake houseboat night.",
         itinerary="Arrive Srinagar, Dal Lake shikara\nGulmarg day trip\nPahalgam sightseeing\nSonmarg day trip\nMughal gardens\nDeparture",
         inclusions="Hotel and houseboat stay\nBreakfast and dinner\nTransfers", exclusions="Flights\nGondola tickets"),
    dict(slug="sample-dubai-getaway", title="Dubai City Getaway (sample)", destination="Dubai", region="international",
         category="holiday", duration_days=5, price_from=48000, is_featured=True, suits_vegetarian=True, suits_halal=True, suits_kids=True,
         summary="Desert safari, Burj Khalifa and a Marina dhow cruise.",
         itinerary="Arrive Dubai, dhow cruise\nCity tour and Burj Khalifa\nDesert safari with dinner\nFree day or Abu Dhabi tour\nDeparture",
         inclusions="Hotel stay\nBreakfast\nAirport transfers\nSightseeing", exclusions="Flights\nVisa"),
    dict(slug="sample-singapore-malaysia-group", title="Singapore and Malaysia Group Tour (sample)", destination="Singapore, Malaysia", region="international",
         category="group", duration_days=7, price_from=72000, suits_vegetarian=True, suits_jain=True, suits_kids=True,
         summary="Fixed-departure group tour with an experienced tour manager.",
         itinerary="Arrive Singapore\nSingapore city and Sentosa\nUniversal Studios\nTravel to Kuala Lumpur\nGenting day trip\nKL city tour\nDeparture",
         inclusions="Hotels\nBreakfast and dinner\nTour manager\nSightseeing", exclusions="Flights\nVisa"),
    dict(slug="sample-munnar-corporate", title="Munnar Corporate Offsite (sample)", destination="Munnar", region="india",
         category="corporate", duration_days=3, price_from=12500, suits_vegetarian=True,
         summary="Team-building offsite with a resort stay and group activities.",
         itinerary="Arrive and welcome session\nTeam activities and bonfire\nSightseeing and departure",
         inclusions="Resort stay\nAll meals\nActivity coordinator\nTransport", exclusions="Flights\nAlcohol"),
    dict(slug="sample-rajasthan-heritage", title="Rajasthan Heritage Circuit (sample)", destination="Rajasthan", region="india",
         category="holiday", duration_days=7, price_from=32000, suits_vegetarian=True, suits_jain=True, suits_seniors=True,
         summary="Jaipur, Jodhpur and Udaipur forts and palaces at a relaxed pace.",
         itinerary="Arrive Jaipur\nJaipur sightseeing\nTravel to Jodhpur\nMehrangarh Fort\nTravel to Udaipur\nCity Palace and lake\nDeparture",
         inclusions="Hotel stay\nBreakfast\nPrivate cab", exclusions="Flights\nMonument entry fees"),
]

for data in SAMPLES:
    slug = data.pop("slug")
    Package.objects.update_or_create(slug=slug, defaults={**data, "is_published": True})

print(f"{len(SAMPLES)} sample packages saved. Total packages now: {Package.objects.count()}")