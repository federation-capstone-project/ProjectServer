from django.urls import path

from . import views
from django.conf.urls import url, include
from rest_framework.views import APIView
from jsonapi.models import *
from jsonapi.views import *
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='Events')
#router.register(r'mycourses', StudentViewSet, basename='Student')
router.register(r'studentevent', StudentEventViewSet, basename='StudentEvents')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^mycourses/(?P<student>.+)/$', MyCourseList.as_view()),
    url(r'^myevents/(?P<student>.+)/$', MyEventsList.as_view()),
    url(r'^api-auth', include('rest_framework.urls'))
]
