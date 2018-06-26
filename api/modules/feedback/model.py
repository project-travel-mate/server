from django.conf import settings
from django.db import models


class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=255, default="Other")
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
