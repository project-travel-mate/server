from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Feedback
from api.modules.feedback.serializers import FeedbackSerializer

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
def get_feedback_all(request):
    """
    This api recieves the call to return the feedback by a curent user in
    descending order of date
    """
    person = request.user
    user_feedback = Feedback.objects.filter(user=person).order_by('-created')
    serializer = FeedbackSerializer(user_feedback)
    return Response(serializer.data)