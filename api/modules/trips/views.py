from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Trip, City
from api.modules.trips.serializers import TripSerializer


@api_view(['POST'])
def add_trip(request):
    trip_name = request.POST.get('trip_name', None)
    start_date = request.POST.get('start_date', None)
    city_id = request.POST.get('city_id', None)

    if not trip_name or not start_date or not city_id:
        # incorrect request received
        error_message = "Missing parameters in request. Send trip_name, city_id, start_date"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    try:
        city = City.objects.get(pk=city_id)
        trip = Trip(trip_name=trip_name, city=city, start_date=start_date)
        trip.save()
        trip.users.add(request.user)
    except Exception as e:
        error_message = str(e)
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    success_message = "Sucessfully added new trip."
    return Response(success_message, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_trip(request, trip_id):
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
    trips = Trip.objects.filter(users=request.user)[:no_of_trips]
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def add_friend_to_trip(request, trip_id, user_id):
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
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        error_message = "User does not exist"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)
