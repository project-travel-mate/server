from rest_framework import serializers

from api.models import Notification
from api.modules.trips.serializers import TripSerializer
from api.modules.users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    initiator_user = UserSerializer(many=False, read_only=True)
    trip = TripSerializer(many=False, read_only=True)

    class Meta(object):
        model = Notification
        fields = ('id', 'initiator_user', 'notification_type', 'text', 'created_at', 'is_read', 'trip')
