from django.shortcuts import render
from api.modules.checklist.serializers import ChecklistSerializer, ChecklistItemSerializer
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import ChecklistItem, Checklist

@api_view(['POST'])
def add_to_checklist(request):
    """
    Adds Items to Checklist, otherwise creates one and adds it to that.
    """

    items = request.POST.get('items', None)
    item_list = items.strip().split(',')
    
    try:
        checklist = Checklist.objects.get(user=request.user)
    except:
        checklist = Checklist(user=request.user)

    for item in item_list:
        try:
            checklist_item = ChecklistItem.objects.get(item=item)
        except:
            checklist_item = ChecklistItem(checklist=checklist, item=item)
            checklist_item.save()

        checklist.items.add(checklist_item)  
    
    checklist.save()
    success_message = "Successfully added to checklist"
    return Response(success_message, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_checklist(request):
    """
    Fetches the Checklist if it exists.
    """
    try:
        checklist = Checklist.objects.get(user=request.user)
    except:
        error_message = "No Checklist exists for this user."
        return Response(error_message)
    serializer = ChecklistSerializer(checklist)
    return Response(serializer.data)