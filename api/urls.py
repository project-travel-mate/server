from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken import views as auth_views

from api.modules.users import views as user_views
from api.modules.city import views as city_views
from api.modules.weather import views as weather_views
from api.modules.shopping import views as shopping_views

urlpatterns = [
    # Authentication
    url(r'^sign-up', user_views.sign_up, name='sign-up'),
    url(r'^sign-in', auth_views.obtain_auth_token, name='sign-in'),

    # Users
    path('get-user/<str:email>', user_views.get_user, name='get-user'),

    # City APIs
    path('get-all-cities', city_views.get_all_cities, name='get-all-cities'),
    path('get-all-cities/<int:no_of_cities>', city_views.get_all_cities, name='get-all-cities'),
    path('get-city/<int:city_id>', city_views.get_city, name='get-city'),
    path('get-city-images/<int:city_id>', city_views.get_all_city_images, name='get-city-images'),
    path('get-city-facts/<int:city_id>', city_views.get_all_city_facts, name='get-city-facts'),
    path('get-city-trends/<int:city_id>', city_views.get_city_trends, name='get-city-trends'),

    # Weather APIs
    path('get-city-weather/<str:city_name>', weather_views.get_city_weather, name='get-city-weather'),
    path('get-multiple-days-weather/<int:num_of_days>/<str:city_name>', weather_views.get_multiple_days_weather,
         name='get-multiple-days-weather'),

    # Shopping APIs
    path('get-shopping-info/<str:query>', shopping_views.get_shopping_info, name="get-shopping-info")
]
