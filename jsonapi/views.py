#from django.shortcuts import render
#from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from . import models
from .models import *
from rest_framework import generics


class MyEventsList(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        student = self.kwargs['student']
        the_student = Student.objects.filter(id=student)
        courses = the_student.values_list('student_courses')
        return Event.objects.filter(event_course__in=courses)

class MyCourseList(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(id=self.kwargs['student'])
