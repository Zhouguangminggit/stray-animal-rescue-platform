from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import health, home

urlpatterns = [
    path("health/", health, name="health"),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("animals/", include("apps.animals.urls")),
    path("adoptions/", include("apps.adoptions.urls")),
    path("community/", include("apps.volunteers.urls")),
    path("donations/", include("apps.donations.urls")),
    path("activities/", include("apps.activities.urls")),
    path("", home, name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
