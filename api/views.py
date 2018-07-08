from django.shortcuts import redirect
from django.template import RequestContext


def view_404(request):
    return redirect('/')


def view_home(request):
    return redirect('http://project-travel-mate.github.io/Travel-Mate/')
