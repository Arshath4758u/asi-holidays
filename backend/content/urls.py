from django.urls import path

from .views import PolicyListView, SiteSettingsView

urlpatterns = [
    path("site/", SiteSettingsView.as_view()),
    path("policies/", PolicyListView.as_view()),
]