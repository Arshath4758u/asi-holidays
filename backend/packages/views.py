from rest_framework import generics

from .models import Package
from .serializers import PackageDetailSerializer, PackageListSerializer


class PackageListView(generics.ListAPIView):
    serializer_class = PackageListSerializer
    pagination_class = None

    def get_queryset(self):
        qs = Package.objects.filter(is_published=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        if self.request.query_params.get("featured") == "1":
            qs = qs.filter(is_featured=True)
        return qs


class PackageDetailView(generics.RetrieveAPIView):
    serializer_class = PackageDetailSerializer
    lookup_field = "slug"
    queryset = Package.objects.filter(is_published=True)
