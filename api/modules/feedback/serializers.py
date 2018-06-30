from rest_framework import serializers
from api.models import Feedback
from api.modules.users.serializers import UserSerializer

""" This serializer is here for sending the feedback model data in json format """


class FeedbackIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id', 'text', 'type', 'created')


""" This is different because we have a user column which is a foreign key having one to many relation """


class FeedbackSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ('id', 'text', 'created', 'users', 'type')
