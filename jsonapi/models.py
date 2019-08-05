from django.db import models
from rest_framework import routers, serializers, viewsets

# Create your models here.

# this fucker has some utility shit for json
# this may or may not be a good idea

class Event(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.CharField(max_length=200)
    room = models.CharField(max_length=200)
    mac = models.CharField(max_length=200)
    time = models.DateTimeField('Starting time')
    repeating = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title + " - " + self.teacher

class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title', 'room']

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class Student(models.Model):
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    student_phone = models.CharField(max_length=200)
    student_email = models.CharField(max_length=200)
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

class StudentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = ['student', 'event', 'attended']

class StudentEventViewSet(viewsets.ModelViewSet):
    queryset = queryset = StudentEvent.objects.none()
    serializer_class = StudentEventSerializer

class Clinician(models.Model):
    clinician_name = models.CharField(max_length=200)
    staff_id = models.CharField(max_length=200)
    staff_email = models.CharField(max_length=200)
    staff_mac_address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.clinician_name
