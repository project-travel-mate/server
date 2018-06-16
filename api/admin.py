from django.contrib import admin

from api.models import City, CityImage, CityFact, Trip

admin.site.register(City)
admin.site.register(CityImage)
admin.site.register(CityFact)
admin.site.register(Trip)
