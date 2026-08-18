from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def healthz(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("healthz/", healthz, name="healthz"),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.training.urls")),
    path("api/", include("apps.gamification.urls")),
]
