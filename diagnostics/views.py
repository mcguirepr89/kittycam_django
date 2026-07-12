import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from cameras.models import Camera
from diagnostics.services.go2rtc import get_stream_status


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


    print("=== Diagnostics Request ===")
    print(f"Camera: {camera.name}")
    print(f"Browser can reach go2rtc: {browser_reachable}")


    #
    # For now, only test the go2rtc API if the browser
    # says it can reach the endpoint.
    #
    if browser_reachable:

        status = get_stream_status(camera)

        print("go2rtc status:")
        print(status)

    else:

        status = {
            "status": "browser_cannot_reach_go2rtc"
        }

        print("Skipping go2rtc API test.")


    print("===========================")


    return JsonResponse(
        {
            "success": True,
            "camera": camera.name,
            "browser_reachable": browser_reachable,
            "go2rtc_status": status,
        }
    )
