from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models
from .models import *
import json

# Create your views here.
# def index(request):
#     event_data = []
#     for event in Event.objects.all():
#         event_data.append({
#             'title': event.title,
#             'teacher': event.teacher,
#             'room': event.room,
#             'time': event.time.isoformat(),
#             'repeating':event.repeating,
#             'mac':event.mac
#         })
#     return HttpResponse(json.dumps(event_data))

# def post(request):
#     if request.method == 'POST':
#         post_data = json.loads(request.body)
#         new_event = Event.objects.create(
#                 title = "test",
#                 teacher = "test",
#                 room = "test",
#                 mac = "test",
#                 time = DateTime.now(),
#                 repeating = True)
#         return HttpResponse("Event Created")
#     return HttpResponse("Event Creation Error")

class StudentList(APIView):
    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#change this to return all of the students attendance records
class StudentEventView(APIView):
    def get(self, request, format=None):
        studentevents = StudentEvents.objects.none()
        serializer = StudentSerializer(students)

    def post(self, request, format=None):
        serializer = StudentEventSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)