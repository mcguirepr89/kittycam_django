from diagnostics.engine import DiagnosticResult
from diagnostics.services.go2rtc import get_stream_status


def run_diagnostics(camera, browser_reachable):
    """
    Run all applicable diagnostics for a camera.

    Returns:
        list[DiagnosticResult]
    """

    results = []

    #
    # Browser connectivity
    #
    if browser_reachable:

        results.append(
            DiagnosticResult(
                name="browser",
                success=True,
                status="reachable",
                summary="Browser can reach go2rtc.",
            )
        )

    else:

        results.append(
            DiagnosticResult(
                name="browser",
                success=True,
                status="unreachable",
                summary="Browser cannot reach go2rtc.",
            )
        )

        #
        # Nothing else makes sense to test.
        #
        return results

    #
    # go2rtc diagnostic
    #
    go2rtc = get_stream_status(camera)

    summaries = {
        "healthy": "Stream is healthy.",
        "authentication_failed": "go2rtc could not authenticate with the camera.",
        "camera_unreachable": "Camera could not be reached.",
        "camera_timeout": "Camera did not respond.",
        "misconfigured_rtsp_url": "The RTSP URL is misconfigured.",
        "no_producers": "No producers are available.",
        "go2rtc_unreachable": "Django could not reach go2rtc.",
        "go2rtc_error": "go2rtc returned an error.",
    }

    results.append(
        DiagnosticResult(
            name="go2rtc",
            success=go2rtc["success"],
            status=go2rtc["status"],
            summary=summaries.get(
                go2rtc["status"],
                "Unknown go2rtc status.",
            ),
            details=go2rtc["message"],
            metadata={
                "api_url": go2rtc["api_url"],
                "producer": go2rtc["producer"],
            },
        )
    )

    return results
