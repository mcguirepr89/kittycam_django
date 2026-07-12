from diagnostics.engine.diagnostics import browser
from diagnostics.engine.diagnostics import go2rtc


def run_diagnostics(camera, browser_reachable):
    """
    Run all applicable diagnostics for a camera.

    The runner is responsible only for orchestration.

    Each diagnostic module is responsible for performing one diagnostic
    and returning a DiagnosticResult.

    Returns:
        list[DiagnosticResult]
    """

    results = []

    #
    # Browser connectivity.
    #
    browser_result = browser.run(browser_reachable)

    results.append(browser_result)

    #
    # If the browser cannot reach go2rtc, there is no point
    # in executing additional diagnostics.
    #
    if browser_result.status != "reachable":

        return results

    #
    # go2rtc connectivity.
    #
    go2rtc_result = go2rtc.run(camera)

    results.append(go2rtc_result)

    #
    # Future diagnostics will be conditionally executed here.
    #
    # Example:
    #
    # if go2rtc_result.status == "camera_timeout":
    #     results.append(rtsp.run(camera))
    #
    # if go2rtc_result.status == "camera_unreachable":
    #     results.append(ping.run(camera))
    #

    return results
