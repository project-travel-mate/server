from django.conf import settings
from django.db import models


class Trip(models.Model):
    trip_name = models.CharField(max_length=128)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    start_date_tx = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
