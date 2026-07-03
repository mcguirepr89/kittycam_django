from django.db import models


class Camera(models.Model):
    name = models.CharField(max_length=100)

    stream_url = models.URLField()

    enabled = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
