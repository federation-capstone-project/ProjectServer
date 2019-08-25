from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models
from .models import *
import json

class EventList(APIView):
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class StudentList(APIView):
#     def get(self, request, format=None):
#         students = Student.objects.none()
#         serializer = StudentSerializer(students, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = StudentSerializer(data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#change this to return all of the students attendance records
# class StudentEventView(APIView):
#     def get(self, request, format=None):
#         studentevents = StudentEvents.objects.all()
#         serializer = StudentEventSerializer(students)

#     def post(self, request, format=None):
#         serializer = StudentEventSerializer(data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
