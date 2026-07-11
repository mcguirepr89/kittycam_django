from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("diagnostics/", include("diagnostics.urls")),
    path("", include("dashboard.urls")),
]
