from enum import Enum

from django.db import models
from django.contrib.auth.models import User


class NotificationTypeChoice(Enum):
    COMMON = "Common"
    TRIP = "Trip"

    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class Notification(models.Model):
    initiator_user = models.ForeignKey(
        User,
        related_name='initiator_user',
        on_delete=models.CASCADE
    )
    destined_user = models.ForeignKey(
        User,
        related_name='destined_user',
        on_delete=models.CASCADE
    )
    notification_type = models.CharField(
        max_length=100,
        default=NotificationTypeChoice.COMMON.value,
        choices=NotificationTypeChoice.choices()
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, null=True, default=None)
