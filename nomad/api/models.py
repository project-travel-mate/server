from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.TextField(null=True, blank=True)
    total_trips = models.IntegerField(default=0)

    def as_json(self):
        return dict(
            id=self.id,
            city_name=self.city_name,
            description=self.description,
            latitude=str(self.latitude),
            longitude=str(self.longitude),
            image=self.image,
            total_trips=self.total_trips
        )
