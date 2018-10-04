from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.models import Notification, NotificationTypeChoice
from api.modules.notification.serializers import NotificationSerializer


def add_notification(initiator_user, destined_user, text, notification_type=NotificationTypeChoice.COMMON.value,
                     trip=None):
    """
    Add Notification for user
    :param request:
    :param initiator_user:
    :param destined_user:
    :param text:
    :param notification_type:
    :param trip: Optional Parameter
    :return: True if notification created
    :return: False if error occurs
    """
    try:
        notification = Notification(
            initiator_user=initiator_user,
            destined_user=destined_user,
            text=text,
            notification_type=notification_type,
        )
        if notification_type == NotificationTypeChoice.TRIP.value:
            notification.trip = trip
        notification.save()
    except Exception:
        return False  # Failed to create notification
    return True  # Notification successfully Created


@api_view(['GET'])
def get_notifications(request):
    """
    Display all notification for request user
    :param request:
    :return: 200 successful
    """
    notifications = Notification.objects.filter(destined_user=request.user).order_by('-created_at')
    paginator = PageNumberPagination()
    paginator.page_size = 10
    notifications_paginated = paginator.paginate_queryset(notifications, request)
    serializer = NotificationSerializer(notifications_paginated, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def mark_notification_as_read(request, notification_id):
    """
    Mark notification as read
    :param request:
    :param notification_id:
    :return 200 successful
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        if request.user != notification.destined_user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        notification.is_read = True
        notification.save()

    except Notification.DoesNotExist:
        error_message = "Notification does not exist"
        return Response(error_message, status=status.HTTP_404_NOT_FOUND)

    success_message = "Successfully marked notification as read."
    return Response(success_message, status=status.HTTP_200_OK)


@api_view(['GET'])
def mark_all_notification_as_read(request):
    """
    Mark all notification as read
    :param request:
    :return 200 successful
    """
    notifications = Notification.objects.filter(destined_user=request.user)
    notifications.update(is_read=True)
    success_message = "Successfully marked all notifications as read."
    return Response(success_message, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_number_of_unread_notifications(request):
    """
    Return number of unread notification for user
    :param request:
    :return 200 successful:
    """
    response = {}
    no_of_notifications = Notification.objects.filter(
        destined_user=request.user,
        is_read=False
    ).count()
    response['number_of_unread_notifications'] = no_of_notifications
    return Response(response, status=status.HTTP_200_OK)
