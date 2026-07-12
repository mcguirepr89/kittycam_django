import json

from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse, urlunparse
from urllib.request import urlopen


REQUEST_TIMEOUT = 5


def _build_api_url(viewer_url):
    """
    Convert a go2rtc viewer URL into its corresponding API endpoint.

    Example:

        https://kittycam.internal/stream.html?src=kittycam

    becomes:

        https://kittycam.internal/api/streams?src=kittycam&video=all&audio=all&microphone
    """

    parsed = urlparse(viewer_url)
    stream_name = parse_qs(parsed.query)["src"][0]

    return urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            "/api/streams",
            "",
            f"src={stream_name}&video=all&audio=all&microphone",
            "",
        )
    )


def _result(api_url, *, success, producer, status, message=None):
    """
    Return a consistently structured diagnostics response.
    """

    return {
        "success": success,
        "api_url": api_url,
        "producer": producer,
        "status": status,
        "message": message,
    }


def _classify_text_response(api_url, text):
    """
    Interpret plain-text responses returned by go2rtc.
    """

    text = text.strip()

    ERROR_PATTERNS = {
        "wrong user/pass": "authentication_failed",
        "no route to host": "camera_unreachable",
        "i/o timeout": "camera_timeout",
        "invalid userinfo": "misconfigured_rtsp_url",
    }

    for pattern, status in ERROR_PATTERNS.items():
        if pattern in text:
            return _result(
                api_url,
                success=True,
                producer=False,
                status=status,
                message=text,
            )

    return _result(
        api_url,
        success=True,
        producer=False,
        status="go2rtc_error",
        message=text,
    )


def get_stream_status(camera):
    """
    Query go2rtc for the current status of a stream.
    """

    api_url = _build_api_url(camera.viewer_url)

    #
    # Retrieve response from go2rtc.
    #
    try:

        with urlopen(api_url, timeout=REQUEST_TIMEOUT) as response:
            raw_body = response.read().decode("utf-8")

    except HTTPError as exc:

        body = exc.read().decode("utf-8")
        return _classify_text_response(api_url, body)

    except TimeoutError:

        return _result(
            api_url,
            success=True,
            producer=False,
            status="camera_timeout",
            message="Timed out waiting for go2rtc.",
        )

    except URLError as exc:

        return _result(
            api_url,
            success=False,
            producer=False,
            status="go2rtc_unreachable",
            message=str(exc),
        )

    #
    # Try to parse a normal JSON response.
    #
    try:

        payload = json.loads(raw_body)

    except json.JSONDecodeError:

        return _classify_text_response(api_url, raw_body)

    #
    # Successful JSON response.
    #
    producers = payload.get("producers", [])

    if producers:

        return _result(
            api_url,
            success=True,
            producer=True,
            status="healthy",
        )

    return _result(
        api_url,
        success=True,
        producer=False,
        status="no_producers",
    )
