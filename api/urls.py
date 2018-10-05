from django.conf.urls import url
from django.urls import path
from rest_framework.authtoken import views as auth_views

from api.modules.analytics import views as analytics_views
from api.modules.city import views as city_views
from api.modules.currency import views as currency_views
from api.modules.feedback import views as feedback_views
from api.modules.food import views as food_views
from api.modules.github import views as github_views
from api.modules.hyperlocal import views as places_views
from api.modules.notification import views as notification_views
from api.modules.shopping import views as shopping_views
from api.modules.static import views as static_views
from api.modules.trips import views as trip_views
from api.modules.twitter import views as twitter_views
from api.modules.users import views as user_views
from api.modules.weather import views as weather_views

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
    path('update-password', user_views.update_password, name='update-password'),
    path('remove-profile-image', user_views.remove_profile_image, name='remove-profile-image'),
    path('remove-user-status', user_views.remove_user_status, name='remove-user-status'),
    path('forgot-password-email-code', user_views.forgot_password_email_code, name='forgot-password-email-code'),
    path('forgot-password-verify-code/<str:code>/<str:new_password>', user_views.forgot_password_verify_code,
         name='forgot-password-verify-code-code'),
    path('delete-profile', user_views.delete_profile, name='delete-profile'),

    # City APIs
    path('get-all-cities', city_views.get_all_cities, name='get-all-cities'),
    path('get-all-cities/<int:no_of_cities>', city_views.get_all_cities, name='get-all-cities'),
    path('get-city/<int:city_id>', city_views.get_city, name='get-city'),
    path('get-city-by-name/<str:city_prefix>', city_views.get_city_by_name, name='get-city-by-name'),
    path('get-city-images/<int:city_id>', city_views.get_all_city_images, name='get-city-images'),
    path('get-city-facts/<int:city_id>', city_views.get_all_city_facts, name='get-city-facts'),
    path('get-city-information/<int:city_id>', city_views.get_city_information, name="get-city-information"),
    path('get-visited-city', city_views.get_visited_city, name='get-visited-city'),
    path('get-visited-city/<int:user_id>', city_views.get_visited_city, name='get-visited-city'),
    path('add-city-nickname', city_views.add_city_nickname, name="add-city-nickname"),

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
    path('get-common-trips/<int:user_id>', trip_views.get_common_trips, name="get-common-trips"),
    path('remove-user-from-trip/<int:trip_id>', trip_views.remove_user_from_trip, name="remove-user-from-trip"),

    # Notification
    path('get-notifications', notification_views.get_notifications, name="get-notifications"),
    path('mark-notification/<int:notification_id>',
         notification_views.mark_notification_as_read,
         name="mark-notification"),
    path('mark-all-notification',
         notification_views.mark_all_notification_as_read,
         name="mark-all-notification"),
    path('number-of-unread-notifications',
         notification_views.get_number_of_unread_notifications,
         name="number-of-unread-notifications"),

    # Feedback
    path('add-feedback', feedback_views.add_feedback, name="add-feedback"),
    path('get-all-user-feedback', feedback_views.get_all_user_feedback, name="get-all-user-feedback"),
    path('get-feedback/<int:feedback_id>', feedback_views.get_feedback, name="get-feedback"),

    # Currency Conversion
    path('get-currency-conversion-rate/<str:source_currency_code>/<str:target_currency_code>',
         currency_views.get_currency_exchange_rate, name="get-conversion-rate"),
    path('get-all-currency-rate/<str:start_date>/<str:end_date>/<str:source_currency_code>/<str:target_currency_code>',
         currency_views.get_all_currency_exchange_rate, name='get-all-currency-rate'),

    # Github API
    path('get-contributors/<str:project>', github_views.get_contributors, name="get-contributors"),
    path('get-issues/<str:project>', github_views.get_issues, name="get-issues"),

    # Twitter API
    path('get-city-trends/<int:city_id>', twitter_views.get_city_trends, name='get-city-trends'),
    path('get-search-tweets/<str:query>', twitter_views.get_search_tweets, name='get-search-tweets'),

    # Zomato API
    path('get-all-restaurants/<str:latitude>/<str:longitude>', food_views.get_all_restaurants,
         name="get-all-restaurants"),
    path('get-restaurant/<int:restaurant_id>', food_views.get_restaurant, name="get-restaurant"),

    # Hyperlocal API
    path('get-places/<str:latitude>/<str:longitude>/<str:places_query>', places_views.get_places, name='get-places'),

    # Analytics API
    path('get-total-users', analytics_views.get_total_users, name="get-total-users"),

    # Static API
    path('about-us', static_views.get_about_us, name="get-about-us"),
    path('help', static_views.get_help, name="get-help")
]
