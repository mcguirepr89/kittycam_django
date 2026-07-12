import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cameras.models import Camera
from diagnostics.engine import run_diagnostics


@require_POST
def start_diagnostics(request):

    try:
        payload = json.loads(request.body)

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON",
            },
            status=400,
        )

    camera_id = payload.get("camera_id")
    browser_reachable = payload.get("go2rtc_reachable")

    try:
        camera = Camera.objects.get(pk=camera_id)

    except Camera.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "error": "Camera not found",
            },
            status=404,
        )

    results = run_diagnostics(
        camera=camera,
        browser_reachable=browser_reachable,
    )

    print("=== Diagnostics Request ===")
    print(f"Camera: {camera.name}")

    for result in results:

        print(f"[{result.name}]")
        print(f"  Success : {result.success}")
        print(f"  Status  : {result.status}")
        print(f"  Summary : {result.summary}")

        if result.details:
            print(f"  Details : {result.details}")

        if result.metadata:
            print(f"  Metadata: {result.metadata}")

    print("===========================")

    return JsonResponse(
        {
            "success": True,
            "camera": camera.name,
            "results": [
                result.to_dict()
                for result in results
            ],
        }
    )
