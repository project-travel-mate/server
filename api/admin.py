from django.contrib import admin

from api.models import City, CityImage, CityFact, Trip, Feedback, Profile, Notification

admin.site.register(City)
admin.site.register(CityImage)
admin.site.register(CityFact)
admin.site.register(Trip)
admin.site.register(Feedback)
admin.site.register(Profile)
admin.site.register(Notification)
