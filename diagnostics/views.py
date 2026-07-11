import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def start_diagnostics(request):
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid JSON.",
            },
            status=400,
        )

    print("Diagnostics request:", payload)

    return JsonResponse(
        {
            "success": True,
            "received": payload,
        }
    )
