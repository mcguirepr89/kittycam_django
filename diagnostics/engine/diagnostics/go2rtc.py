from diagnostics.engine import DiagnosticResult
from diagnostics.services.go2rtc import get_stream_status


SUMMARIES = {
    "healthy":
        "Stream is healthy.",

    "authentication_failed":
        "go2rtc could not authenticate with the camera.",

    "camera_unreachable":
        "Camera could not be reached.",

    "camera_timeout":
        "Camera did not respond.",

    "misconfigured_rtsp_url":
        "The RTSP URL is misconfigured.",

    "no_producers":
        "No producers are available.",

    "go2rtc_unreachable":
        "Django could not reach go2rtc.",

    "go2rtc_error":
        "go2rtc returned an error.",
}


def run(camera):
    """
    Run the go2rtc diagnostic.

    Returns:
        DiagnosticResult
    """

    result = get_stream_status(camera)

    return DiagnosticResult(
        name="go2rtc",
        success=result["success"],
        status=result["status"],
        summary=SUMMARIES.get(
            result["status"],
            "Unknown go2rtc status.",
        ),
        details=result["message"],
        metadata={
            "api_url": result["api_url"],
            "producer": result["producer"],
        },
    )
