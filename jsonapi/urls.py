from django.urls import path

from . import views
from django.conf.urls import url, include
from rest_framework.views import APIView
from jsonapi.models import *
from jsonapi.views import *
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='Events')
router.register(r'students', StudentViewSet, basename='Students')
#router.register(r'studentevents', StudentEventViewSet, basename='StudentEvents')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth', include('rest_framework.urls'))
]
