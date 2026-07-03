from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cameras.models import Camera

@login_required
def dashboard(request):
    kittycam = Camera.objects.filter(name__iexact="kittycam").first()
    
    context = {
        "kittycam": kittycam,
    }
    return render(request, "dashboard/dashboard.html", context)
