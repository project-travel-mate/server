from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Trip, City, NotificationTypeChoice
from api.modules.trips.serializers import TripSerializer
from api.modules.notification.views import add_notification


@api_view(['POST'])
def add_trip(request):
    """
    Add a trip with current user as a default member to it
    :param request:
    :return: 400 if incorrect parameters are sent or database request failed
    :return: 201 successful
    """
    trip_name = request.POST.get('trip_name', None)
    start_date_tx = request.POST.get('start_date_tx', None)
    city_id = request.POST.get('city_id', None)

    if not trip_name or not start_date_tx or not city_id:
        # incorrect request received
        error_message = "Missing parameters in request. Send trip_name, city_id, start_date_tx"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    try:
        city = City.objects.get(pk=city_id)
        trip = Trip(trip_name=trip_name, city=city, start_date_tx=start_date_tx)
        trip.save()
        trip.users.add(request.user)
    except Exception as e:
        error_message = str(e)
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    success_message = "Sucessfully added new trip."
    return Response(success_message, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_trip(request, trip_id):
    """
    Returns a trip using 'trip_id'
    :param request:
    :param trip_id:
    :return: 401 if user is not a member of this specific trip
    :return: 404 if invalid trip id is sent
    :return: 200 successful
    """
    try:
        trip = Trip.objects.get(pk=trip_id)
        if request.user not in trip.users.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except Trip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TripSerializer(trip)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_trips(request, no_of_trips=10):
    """
    Returns a list of all the trips for a given user
    :param request:
    :param no_of_trips: default 10
    :return: 200 successful
    """
    trips = Trip.objects.filter(users=request.user)[:no_of_trips]
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def add_friend_to_trip(request, trip_id, user_id):
    """
    Associates a user to existing trip
    :param request:
    :param trip_id:
    :param user_id:
    :return: 400 if trip or user does not exist or user is already associated with the trip
    :return: 401 if current user is not associated with the specific trip
    :return: 200 successful
    """
    try:
        trip = Trip.objects.get(pk=trip_id)
        if request.user not in trip.users.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(pk=user_id)
        if user in trip.users.all():
            error_message = "User already associated with trip"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        trip.users.add(user)
        # creating notification
        notification_text = "You are added to %s trip by %s %s." % (
            trip.city.city_name,
            request.user.first_name,
            request.user.last_name,)
        if not (add_notification(
                initiator_user=request.user,
                destined_user=user,
                text=notification_text,
                notification_type=NotificationTypeChoice.TRIP.value,)):
            raise RuntimeError("Error while creating notification")
    except Trip.DoesNotExist:
        error_message = "Trip does not exist"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        error_message = "User does not exist"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
