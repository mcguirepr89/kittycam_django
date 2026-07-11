from django.urls import path

from . import views

app_name = "diagnostics"

urlpatterns = [
    path("start/", views.start_diagnostics, name="start"),
]
