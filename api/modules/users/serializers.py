from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User object serializer class
    """
    image = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta(object):
        model = User
        fields = ('username', 'first_name', 'last_name', 'id', 'image', 'date_joined', 'status')

    def get_image(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.profile_image
        return None

    def get_status(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.status
        return None


class UserOnlySerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = User
        fields = ('username', 'name')
