from rest_framework import serializers
from api.models import Checklist, ChecklistItem


class ChecklistItemSerializer(serializers.ModelSerializer):
    """
    Serializes used to serialize ChecklistItem data
    """
    class Meta:
        model = ChecklistItem
        fields = ('id', 'item')


class ChecklistSerializer(serializers.ModelSerializer):
    """
    Serializer used to serialize Checklist data
    """
    user = serializers.RelatedField(source='obj.user.username', read_only=True)
    items = ChecklistItemSerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = ('id', 'user', 'items')
