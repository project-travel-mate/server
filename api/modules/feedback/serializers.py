from rest_framework import serializers
from api.models import Feedback
from api.modules.users.serializers import UserSerializer
   

class FeedbackIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id','text', 'type', 'created')

class FeedbackSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ('id','created','users','type')
