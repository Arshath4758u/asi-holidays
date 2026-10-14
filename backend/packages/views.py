from rest_framework import generics

from .models import Package
from .serializers import PackageDetailSerializer, PackageListSerializer

# ?food=veg,jain  and  ?with=kids  map to boolean columns
FOOD_FIELDS = {"veg": "suits_vegetarian", "jain": "suits_jain", "halal": "suits_halal"}
WITH_FIELDS = {"kids": "suits_kids", "seniors": "suits_seniors"}


class PackageListView(generics.ListAPIView):
    """
    Filters (all optional, comma-separated):
      region=india,international        -> match ANY
      category=honeymoon,family         -> match ANY
      food=veg,jain,halal               -> match ALL
      with=kids,seniors                 -> match ALL
      featured=1
    """

    serializer_class = PackageListSerializer
    pagination_class = None

    def _csv(self, name):
        return [v for v in self.request.query_params.get(name, "").split(",") if v]

    def get_queryset(self):
        qs = Package.objects.filter(is_published=True)
        regions = self._csv("region")
        if regions:
            qs = qs.filter(region__in=regions)
        categories = self._csv("category")
        if categories:
            qs = qs.filter(category__in=categories)
        for key in self._csv("food"):
            if key in FOOD_FIELDS:
                qs = qs.filter(**{FOOD_FIELDS[key]: True})
        for key in self._csv("with"):
            if key in WITH_FIELDS:
                qs = qs.filter(**{WITH_FIELDS[key]: True})
        if self.request.query_params.get("featured") == "1":
            qs = qs.filter(is_featured=True)
        return qs


class PackageDetailView(generics.RetrieveAPIView):
    serializer_class = PackageDetailSerializer
    lookup_field = "slug"
    queryset = Package.objects.filter(is_published=True)