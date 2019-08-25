from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import routers, serializers, viewsets
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

# this fucker has some utility shit for json
# this may or may not be a good idea

# I tried hooking the save event but now I'm trying extending abstract user, FML I have assignments to complete.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'administrator'),
        (2, 'clinician'),
        (3, 'student'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)
        
class Clinician(models.Model):
    clinician_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    clinician_name = models.CharField(max_length=200)
    clinician_id = models.CharField(max_length=200)
    clinician_phone = PhoneNumberField()
    clinician_email = models.EmailField()
    clinician_mac = models.CharField(max_length=200)
    
    def __str__(self):
        return self.clinician_name

class ClinicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinician
        fields = ['clinician_name', 'clinician_mac']

class ClinicianViewSet(viewsets.ModelViewSet):
    queryset = Clinician.objects.all()
    serializer_class = ClinicianSerializer

class Course(models.Model):
    course_code = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_code + " - " + self.course_name

class Event(models.Model):
    event_title = models.CharField(max_length=200)
    event_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    event_clinician = models.ForeignKey(Clinician, on_delete=models.PROTECT)
    event_location = models.CharField(max_length=200)
    event_starttime = models.DateTimeField('Starting time')
    event_finishtime = models.DateTimeField('Ending time')
    event_repeating = models.BooleanField(default=True)
    event_frequency = models.PositiveSmallIntegerField()

    #event_mac = self.event_clinician.clinician_mac
    
    def __str__(self):
        return self.title# + " - " + Clinician.objects.filter(id=teacher).clinician_name#self.teacher.clinician_name

class EventSerializer(serializers.ModelSerializer):
    event_code = serializers.RelatedField(source='event_course', read_only=True)
    clinician_name = serializers.RelatedField(source='event_clinician', read_only=True)
    clinician_mac = serializers.RelatedField(source='event_clinician', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id','event_title', 'event_code', 'event_clinician', 'clinician_name', 'clinician_mac', 'event_starttime', 'event_finishtime', 'event_repeating', 'event_frequency']

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class Student(models.Model):
    student_courses = models.ManyToManyField(Course)
    student_user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    student_phone = PhoneNumberField()
    student_email = models.EmailField()
    student_percent = models.CharField(max_length=200)
    
    def __str__(self):
        return self.student_name + " - " + self.student_id

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id','student_name','student_phone','student_email','student_percent']

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    attended = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)

    def __str__(self):
        return self.event.title + " - " + self.student.student_name

class StudentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = ['student', 'event', 'attended', 'manual']

class StudentEventViewSet(viewsets.ModelViewSet):
    queryset = queryset = StudentEvent.objects.none()
    serializer_class = StudentEventSerializer
