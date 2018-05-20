import json

from django.http import HttpResponse
from django.core import serializers

from django.shortcuts import render

from api.models import City


def index(request):
    latest_question_list = City.objects.all()
    print(latest_question_list)
    # output = ', '.join([q.question_text for q in latest_question_list])
    results = [ob.as_json() for ob in latest_question_list]
    return HttpResponse(json.dumps(results), content_type="application/json")
    # return serializers.serialize('json', [ latest_question_list, ])
    # return HttpResponse("Hello, world. You're at the polls index.")
