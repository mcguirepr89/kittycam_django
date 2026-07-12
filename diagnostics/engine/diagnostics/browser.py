from diagnostics.engine import DiagnosticResult


def run(browser_reachable):
    """
    Run the browser connectivity diagnostic.

    This diagnostic records whether the user's browser was able to
    reach the go2rtc endpoint.

    Returns:
        DiagnosticResult
    """

    if browser_reachable:

        return DiagnosticResult(
            name="browser",
            success=True,
            status="reachable",
            summary="Browser can reach go2rtc.",
        )

    return DiagnosticResult(
        name="browser",
        success=True,
        status="unreachable",
        summary="Browser cannot reach go2rtc.",
    )
