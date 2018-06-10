from django.contrib import admin

from api.modules.city.model import City, CityImage, CityFact

admin.site.register(City)
admin.site.register(CityImage)
admin.site.register(CityFact)
