from smtplib import SMTPException

from django.core.mail import send_mail

from nomad.settings import DEFAULT_EMAIL_SENDER, DEBUG


def is_send_email(to_list, subject, body):
    """
    Tries to send email. If email is sent successfully, returns True else False
    If running app in Debug mode, do not try to send email
    :param to_list:
    :param subject:
    :param body:
    :return: Is sending email success
    """
    if DEBUG:
        return True

    try:
        send_mail(subject, body, DEFAULT_EMAIL_SENDER, to_list, fail_silently=False)
    except SMTPException:
        return False
    return True
