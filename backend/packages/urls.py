from django.urls import path

from .views import PackageDetailView, PackageListView

urlpatterns = [
    path("packages/", PackageListView.as_view()),
    path("packages/<slug:slug>/", PackageDetailView.as_view()),
]
