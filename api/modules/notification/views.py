from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import Notification, NotificationTypeChoice
from api.modules.notification.serializers import NotificationSerializer


def add_notification(initiator_user, destined_user, text, notification_type=NotificationTypeChoice.COMMON.value):
    """
    Add Notification for user
    :param request:
    :param initiator_user:
    :param destined_user:
    :param text:
    :param notification_type:
    :return: True if notification created
    :return: False if error occurs
    """
    try:
        Notification.objects.create(
            initiator_user=initiator_user,
            destined_user=destined_user,
            text=text,
            notification_type=notification_type,
        )
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
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)
