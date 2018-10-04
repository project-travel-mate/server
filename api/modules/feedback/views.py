from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

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
    :return: 401 if authorization failed
    :return: 404 if not found
    :return: 200 successful
    """

    try:
        user_feedback = Feedback.objects.get(pk=feedback_id)
        if request.user is not user_feedback.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    except Feedback.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = FeedbackCondensedSerializer(user_feedback)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_user_feedback(request):
    """
    Returns a list of all the feedbacks for a given user
    :param request:
    :return: 200 successful
    """
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    feedbacks_paginated = paginator.paginate_queryset(feedbacks, request)
    serializer = FeedbackSerializer(feedbacks_paginated, many=True)
    return paginator.get_paginated_response(serializer.data)
