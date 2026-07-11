from urllib.parse import quote

from django.db import models


class Camera(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Friendly name displayed throughout the application.",
    )

    enabled = models.BooleanField(
        default=True,
        help_text="Whether this camera should be available to users.",
    )

    lan_ip = models.GenericIPAddressField(
        protocol="IPv4",
        help_text="LAN IPv4 address of the camera.",
    )

    rtsp_port = models.PositiveIntegerField(
        default=554,
        help_text="RTSP port exposed by the camera.",
    )

    rtsp_username = models.CharField(
        max_length=100,
        help_text="Username used to authenticate to the camera's RTSP server.",
    )

    rtsp_password = models.CharField(
        max_length=255,
        help_text="RTSP password (to be encrypted in a future version).",
    )

    rtsp_path = models.CharField(
        max_length=255,
        help_text="RTSP stream path, beginning with '/'.",
    )

    viewer_url = models.URLField(
        help_text="Public URL that users access to view the stream (typically the go2rtc WebRTC viewer).",
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"

    def __str__(self):
        return self.name

    @property
    def rtsp_url(self):
        """
        Returns the complete RTSP URL for this camera.

        Credentials are URL-encoded so that special characters in the
        username or password do not produce an invalid URL.
        """
        username = quote(self.rtsp_username, safe="")
        password = quote(self.rtsp_password, safe="")

        return (
            f"rtsp://{username}:{password}"
            f"@{self.lan_ip}:{self.rtsp_port}"
            f"{self.rtsp_path}"
        )
