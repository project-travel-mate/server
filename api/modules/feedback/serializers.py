from rest_framework import serializers
from api.models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('id','user','type','text','created')
        read_only_fields = ('id','user')