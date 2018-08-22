from django.utils import timezone

from .models import Profile


class LastActiveMiddleware:
    """
    Custome middleware to update last_active field of Profile model
    on every authenticated api call
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """
        called just after the view has finished executing
        """
        try:
            if request.user.is_authenticated:
                profile = Profile.objects.get(user=request.user)
                profile.last_active = timezone.now()
                profile.save()
        except Exception:
            pass
        return response
