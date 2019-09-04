from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import *
from .forms import *
from rest_framework import generics
from django.http import HttpResponse
from django.contrib.auth import login
from django.views.generic import CreateView

class MyEventsList(generics.ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        student = Student.objects.filter(id=self.kwargs['student'])
        courses = student.values_list('student_courses')
        return Event.objects.filter(event_course__in=courses)

class MyCourseList(generics.ListAPIView):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.filter(id=self.kwargs['student'])

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        status = "success"
        token = Token.objects.create(user=user)
        login(self.request, user)
        return HttpResponse('{"status":"%s", "token":"%s"}' % (status, token.key))

