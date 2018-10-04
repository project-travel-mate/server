from django.conf import settings
from django.core.validators import URLValidator
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    nickname = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    total_trips = models.IntegerField(default=0)
    woeid = models.TextField(null=True, blank=True)  # Yahoo! Where On Earth ID


class CityImage(models.Model):
    city = models.ForeignKey('City', related_name="images", on_delete=models.CASCADE)
    image_url = models.TextField(null=True, blank=True, validators=[URLValidator()])


class CityFact(models.Model):
    city = models.ForeignKey('City', related_name="facts", on_delete=models.CASCADE)
    fact = models.TextField(null=False, blank=False)
    source_text = models.TextField(null=False, blank=False)
    source_url = models.TextField(null=False, blank=False)


class CityVisitLog(models.Model):
    city = models.ForeignKey('City', related_name="logs", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='logs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
