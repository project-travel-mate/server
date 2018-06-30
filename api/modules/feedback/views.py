from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Feedback
from api.modules.feedback.serializers import FeedbackSerializer, FeedbackCondensedSerializer


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
def get_feedback(request, feedback_id):
    """
    Returns the feedback pertaining to a certain feedback id
    :param request:
    :return: 400 if incorrect parameters are sent or database request failed
    :return: 201 successful
    """
    try:
        user_feedback = Feedback.objects.get(pk=feedback_id)

    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FeedbackCondensedSerializer(user_feedback)
    return Response(serializer.data)


""" The many specified here is important because we have a one to many relation and
has to be specified in both the serializer as well as here. """


@api_view(['GET'])
def get_all_user_feedback(request):
    """
    Returns a list of all the feedbacks for a given user
    :param request:
    :return: 200 successful
    """
    try:
        feedbacks = Feedback.objects.filter(user=request.user)
    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)
