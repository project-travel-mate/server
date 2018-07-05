from rest_framework import serializers

from api.models import Notification
from api.modules.users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    initiator_user = UserSerializer(many=False, read_only=True)
    destined_user = UserSerializer(many=False, read_only=True)

    class Meta(object):
        model = Notification
        fields = ('__all__')
