from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import routers, serializers, viewsets

# Create your models here.

# this fucker has some utility shit for json
# this may or may not be a good idea

class Clinician(models.Model):
    clinician_name = models.CharField(max_length=200)
    staff_id = models.CharField(max_length=200)
    staff_phone = PhoneNumberField()
    staff_email = models.EmailField()
    staff_mac_address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.clinician_name

class Event(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(Clinician, on_delete=models.PROTECT)
    room = models.CharField(max_length=200)
    mac = models.CharField(max_length=200)
    time = models.DateTimeField('Starting time')
    repeating = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title# + " - " + Clinician.objects.filter(id=teacher).clinician_name#self.teacher.clinician_name

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title', 'teacher', 'room', 'mac', 'time', 'repeating']

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class Student(models.Model):
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

class StudentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = ['student', 'event', 'attended']

class StudentEventViewSet(viewsets.ModelViewSet):
    queryset = queryset = StudentEvent.objects.none()
    serializer_class = StudentEventSerializer
