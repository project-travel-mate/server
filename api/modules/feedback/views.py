from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Feedback


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
