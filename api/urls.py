from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken import views as auth_views

from api.modules.users import views as user_views
from api.modules.city import views as city_views
from api.modules.shopping import views as shopping_views
from api.modules.weather import views as weather_views
from api.modules.trips import views as trip_views
from api.modules.feedback import views as feedback_views
from api.modules.notification import views as notification_views
from api.modules.currency import views as currency_views
from api.modules.github import views as github_views
from api.modules.twitter import views as twitter_views

urlpatterns = [
    # Authentication
    url(r'^sign-up', user_views.sign_up, name='sign-up'),
    url(r'^sign-in', auth_views.obtain_auth_token, name='sign-in'),

    # Users
    path('get-user', user_views.get_user_profile, name='get-user'),
    path('get-user/<int:user_id>', user_views.get_user_by_id, name='get-user-by-id'),
    path('get-user/<str:email>', user_views.get_users_by_email, name='get-users-by-email'),
    path('update-user-details', user_views.update_user_details, name='update-user-details'),
    path('update-profile-image', user_views.update_profile_image, name='update-profile-image'),
    path('update-user-status', user_views.update_user_status, name='update-user-status'),
    path('remove-profile-image', user_views.remove_profile_image, name='remove-profile-image'),

    # City APIs
    path('get-all-cities', city_views.get_all_cities, name='get-all-cities'),
    path('get-all-cities/<int:no_of_cities>', city_views.get_all_cities, name='get-all-cities'),
    path('get-city/<int:city_id>', city_views.get_city, name='get-city'),
    path('get-city-by-name/<str:city_prefix>', city_views.get_city_by_name, name='get-city-by-name'),
    path('get-city-images/<int:city_id>', city_views.get_all_city_images, name='get-city-images'),
    path('get-city-facts/<int:city_id>', city_views.get_all_city_facts, name='get-city-facts'),
    path('get-city-visits', city_views.get_city_visits, name='get-city-visits'),


    # Weather APIs
    path('get-city-weather/<int:city_id>', weather_views.get_city_weather, name='get-city-weather'),
    path('get-multiple-days-weather/<int:num_of_days>/<str:city_name>', weather_views.get_multiple_days_weather,
         name='get-multiple-days-weather'),

    # Shopping APIs
    path('get-shopping-info/<str:query>', shopping_views.get_shopping_info, name="get-shopping-info"),

    # Trips
    path('add-trip', trip_views.add_trip, name="add-trip"),
    path('get-trip/<int:trip_id>', trip_views.get_trip, name="get-trip"),
    path('get-all-trips', trip_views.get_all_trips, name="get-all-trips"),
    path('get-all-trips/<int:no_of_trips>', trip_views.get_all_trips, name="get-all-trips"),
    path('add-friend-to-trip/<int:trip_id>/<int:user_id>', trip_views.add_friend_to_trip, name="add-friend-to-trip"),
    path('remove-friend-from-trip/<int:trip_id>/<int:user_id>', trip_views.remove_friend_from_trip,
         name="remove-friend-from-trip"),
    path('update-trip-name/<int:trip_id>/<str:trip_name>', trip_views.update_trip_name, name="update-trip-name"),
    path('trip-friends-all', user_views.trip_friends_all, name="trip-friends-all"),

    # Notification
    path('get-notifications', notification_views.get_notifications, name="get-notifications"),
    path('mark-notification/<int:notification_id>',
         notification_views.mark_notification_as_read,
         name="mark-notification"),
    path('mark-all-notification',
         notification_views.mark_all_notification_as_read,
         name="mark-all-notification"),

    # Feedback
    path('add-feedback', feedback_views.add_feedback, name="add-feedback"),
    path('get-all-user-feedback', feedback_views.get_all_user_feedback, name="get-all-user-feedback"),
    path('get-feedback/<int:feedback_id>', feedback_views.get_feedback, name="get-feedback"),

    # Currency Conversion
    path('get-currency-conversion-rate/<str:source_currency_code>/<str:target_currency_code>',
         currency_views.get_currency_exchange_rate, name="get-conversion-rate"),

    # Github API
    path('get-contributors/<str:project>', github_views.get_contributors, name="get-contributors"),
    path('get-issues/<str:project>', github_views.get_issues, name="get-issues"),

    # Twitter API
    path('get-city-trends/<int:city_id>', twitter_views.get_city_trends, name='get-city-trends'),
    path('get-search-tweets/<str:query>', twitter_views.get_search_tweets, name='get-search-tweets'),
]
