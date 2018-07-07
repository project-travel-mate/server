from rest_framework import serializers

from api.models import Trip
from api.modules.city.serializers import CitySerializer
from api.modules.users.serializers import UserSerializer


class TripSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'trip_name', 'city', 'users', 'start_date_tx')


class TripCondensedSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False, read_only=True)
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('id', 'trip_name', 'city', 'users_count', 'start_date_tx')

    def get_users_count(self, obj):
        return obj.users.count()
