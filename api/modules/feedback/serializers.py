from rest_framework import serializers
from api.models import Feedback
from api.modules.users.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):

    #user = UserSerializer(many=False, read_only=True)
    user = serializers.RelatedField(source='user.id', read_only=True)


    class Meta:
        model = Feedback
        fields = ('id','user','type','created')
        read_only=('id','user','type','created')


class FeedbackIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id','text', 'type', 'created')

    
