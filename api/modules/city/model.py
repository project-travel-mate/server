from django.core.validators import URLValidator
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.TextField(null=True, blank=True, validators=[URLValidator()])
    total_trips = models.IntegerField(default=0)
    woeid = models.TextField(null=True, blank=True)  # Yahoo! Where On Earth ID


class CityImage(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    image_url = models.TextField(validators=[URLValidator()])


class CityFact(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    fact = models.TextField(null=False, blank=False)
