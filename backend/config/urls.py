from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "ASI Holidays Admin"
admin.site.site_title = "ASI Holidays"
admin.site.index_title = "Packages and enquiries"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("packages.urls")),
    path("api/", include("enquiries.urls")),
    path("api/", include("content.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
