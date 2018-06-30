from rest_framework import serializers
from api.models import Feedback
from api.modules.users.serializers import UserSerializer

""" This serializer is here for sending the feedback model data in json format """


class FeedbackCondensedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id', 'type', 'created')


""" This is different because we have a user column which is a foreign key having one to many relation """


class FeedbackSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ('id', 'created', 'users', 'type')
