from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Trip, City
from api.modules.trips.serializers import TripSerializer, TripCondensedSerializer


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

    success_message = "Successfully added new trip."
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
    # remove current user from the list of users
    for user in serializer.data['users']:
        if user['id'] == request.user.id:
            serializer.data['users'].remove(user)
            break
    return Response(serializer.data)


@api_view(['GET'])
def get_all_trips(request, no_of_trips=10):
    """
    Returns a list of all the trips for a given user
    :param request:
    :param no_of_trips: default 10
    :return: 200 successful
    """
    trips = Trip.objects.filter(users=request.user).order_by('-start_date_tx')[:no_of_trips]
    serializer = TripCondensedSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def add_friend_to_trip(request, trip_id, user_id):
    """
    Associates a user to existing trip
    :param request:
    :param trip_id:
    :param user_id:
    :return: 400 if user is already associated with the trip
    :return: 404 if trip or user does not exist
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
    except Trip.DoesNotExist:
        error_message = "Trip does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        error_message = "User does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def remove_friend_from_trip(request, trip_id, user_id):
    """
    Dissociates a user to existing trip
    :param request:
    :param trip_id:
    :param user_id:
    :return: 400 if user not present in the trip
    :return: 404 if trip or user does not exist
    :return: 200 successful
    """
    try:
        trip = Trip.objects.get(pk=trip_id)
        if request.user not in trip.users.all():
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(pk=user_id)
        if user not in trip.users.all():
            error_message = "User already not a part of trip"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        trip.users.remove(user)
    except Trip.DoesNotExist:
        error_message = "Trip does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        error_message = "User does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
