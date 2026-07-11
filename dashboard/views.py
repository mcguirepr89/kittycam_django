from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from cameras.models import Camera


@login_required
def dashboard(request):
    cameras = Camera.objects.filter(enabled=True)

    context = {
        "cameras": cameras,
    }

    return render(request, "dashboard/dashboard.html", context)
