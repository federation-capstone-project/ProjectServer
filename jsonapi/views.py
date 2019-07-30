from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import *
import json

# Create your views here.
def index(request):
    event_data = []
    for event in Event.objects.all():
        event_data.append({
            'title': event.title,
            'teacher': event.teacher,
            'room': event.room,
            'time': event.time.isoformat(),
            'repeating':event.repeating,
            'mac':event.mac
        })
    return HttpResponse(json.dumps(event_data))

def post(request):
    if request.method == 'POST':
        post_data = json.loads(request.body)
