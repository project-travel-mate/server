from django.urls import path

from api import views

urlpatterns = [
    path('get-all-cities', views.city.get_all_cities, name='get-all-cities'),
    path('get-city/<int:city_id>', views.city.get_city, name='get-city'),
    path('get-city-images/<int:city_id>', views.city.get_all_city_images, name='get-city-images'),
    path('get-city-facts/<int:city_id>', views.city.get_all_city_facts, name='get-city-facts'),
]
