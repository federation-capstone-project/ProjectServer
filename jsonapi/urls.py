from django.urls import path
from django.conf.urls import url, include
from rest_framework.views import APIView
from .models import *
from .views import *
from rest_framework import routers, serializers, viewsets
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken import views

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='Events')
router.register(r'studentevent', StudentEventViewSet, basename='StudentEvents')

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^api-token-auth/', views.obtain_auth_token),
    url(r'^', include(router.urls)),
    url(r'^signup', StudentSignUpView.as_view(), name='registration'),
    url(r'^mycourses/(?P<student>.+)/$', MyCourseList.as_view()),
    url(r'^myinfo/$', MyStudentInfo.as_view()),
    url(r'^myevents/$', MyEventsList.as_view()),
    url(r'^api-auth', include('rest_framework.urls'))
]
