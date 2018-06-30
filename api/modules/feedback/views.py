from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Feedback
from django.contrib.auth.models import User

from api.modules.feedback.serializers import FeedbackSerializer,FeedbackIDSerializer

@api_view(['POST'])
def add_feedback(request):
    """
    Add a feedback with current user as a default member to it
    :param request:
    :return: 400 if incorrect parameters are sent or database request failed
    :return: 201 successful
    """
    feedback_text = request.POST.get('text', None)
    feedback_type = request.POST.get('type', None)

    if not feedback_text or not feedback_type:
        # incorrect request received
        error_message = "Missing parameters in request. Send text, type"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

    # creating new feedback
    Feedback.objects.create(
        user=request.user,
        text=feedback_text,
        type=feedback_type,
    )

    success_message = "Sucessfully added new feedback."
    return Response(success_message, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_feedback_id(request,feedback_id):
    """
    Returns the feedback pertaining to a certain feedback id
    :param request:
    :return: 400 if incorrect parameters are sent or database request failed
    :return: 201 successful
    """
    try:
        user_feedback = Feedback.objects.get(pk=feedback_id)

    except Feedback.DoesNotExist:
        error_message = "Feedback doesnt exist"
        return Response(error_message,status = status.HTTP_404_NOT_FOUND)
    
    serializer = FeedbackIDSerializer(user_feedback)
    return Response(serializer.data)

""" The many specified here is important because we have a one to many relation and
has to be specified in both the serializer as well as here. """


@api_view(['GET'])
def get_feedback_all(request):
    """
    Returns a list of all the feedbacks for a given user
    :param request:
    :param no_of_trips: default 10
    :return: 200 successful
    """
    try:
        person = Feedback.objects.filter(user=request.user)
    except Feedback.DoesNotExist:
        error_message = "Feedback doesnt exist"
        return Response(error_message,status=status.HTTP_404_NOT_FOUND)
        
    serializer = FeedbackSerializer(person, many=True)
    return Response(serializer.data)
