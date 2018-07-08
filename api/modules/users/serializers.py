from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User object serializer class
    """
    image = serializers.SerializerMethodField()

    class Meta(object):
        model = User
        fields = ('username', 'first_name', 'last_name', 'id', 'image', 'date_joined')

    def get_image(self, obj):
        if hasattr(obj, 'profile'):
            return obj.profile.profile_image
        return None
