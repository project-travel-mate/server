from django.shortcuts import redirect
from nomad.constants import URL_NOT_FOUND_REDIRECT


def view_404(request):
    return redirect('/')


def view_home(request):
    return redirect(URL_NOT_FOUND_REDIRECT)
