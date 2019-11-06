from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import AbstractUser
from datetime import date, timedelta

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'administrator'),
        (2, 'clinician'),
        (3, 'student'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)

class Tile(models.Model):
    tile_name = models.CharField(max_length=200)
    tile_mac = models.CharField(max_length=200)

    def __str__(self):
        return self.tile_name

class Clinician(models.Model):
    clinician_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    clinician_name = models.CharField(max_length=200)
    clinician_id = models.CharField(max_length=200)
    clinician_phone = PhoneNumberField()
    clinician_email = models.EmailField()
    clinician_tile = models.ForeignKey(Tile, on_delete=models.PROTECT)

    def __str__(self):
        return self.clinician_name

class ClinicianSerializer(serializers.ModelSerializer):
    clinician_mac = serializers.ReadOnlyField(source='clinician_tile.tile_mac')

    class Meta:
        model = Clinician
        fields = ['clinician_name', 'clinician_phone', 'clinician_email', 'clinician_mac']

class Course(models.Model):
    course_code = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)

    def __str__(self):
        return self.course_code + " - " + self.course_name

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_code', 'course_name']

class Event(models.Model):
    event_parent = models.ForeignKey('self', blank=True, null=True, default=None, on_delete=models.PROTECT)
    event_title = models.CharField(max_length=200)
    event_course = models.ForeignKey(Course, on_delete=models.PROTECT)
    event_clinician = models.ForeignKey(Clinician, on_delete=models.PROTECT)
    event_location = models.CharField(max_length=200)
    event_starttime = models.DateTimeField('Starting time')
    event_finishtime = models.DateTimeField('Ending time')
    event_repeating = models.BooleanField(default=True)
    event_frequency = models.PositiveSmallIntegerField()
    
    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        if self.event_repeating:
            Event.objects.filter(event_parent=self).delete()
            temp_starttime = self.event_starttime
            while temp_starttime.date() < Config.objects.get(id=1).ending_date:
                temp_starttime += timedelta(days=self.event_frequency)
                child_event = Event.objects.create(
                    event_parent = self,
                    event_title = self.event_title,
                    event_course = self.event_course,
                    event_clinician = self.event_clinician,
                    event_location = self.event_location,
                    event_starttime = temp_starttime,
                    event_finishtime = temp_starttime + timedelta(hours=2),
                    event_repeating = False,
                    event_frequency = self.event_frequency)
                child_event.save()

    def __str__(self):
        return " - ".join([self.event_title, self.event_clinician.clinician_name])

class EventSerializer(serializers.ModelSerializer):
    course_code = serializers.ReadOnlyField(source='event_course.course_code')
    clinician_name = serializers.ReadOnlyField(source='event_clinician.clinician_name')
    clinician_mac = serializers.ReadOnlyField(source='event_clinician.clinician_tile.tile_mac')

    class Meta:
        model = Event
        fields = ['id','event_title', 'course_code', 'event_clinician', 'clinician_name', 'clinician_mac', 'event_location', 'event_starttime', 'event_finishtime', 'event_repeating', 'event_frequency']

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class Student(models.Model):
    student_user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)
    student_phone = PhoneNumberField()
    student_email = models.EmailField()
    student_courses = models.ManyToManyField(Course)
    student_events = models.ManyToManyField(Event, through='StudentEvent')

    @property
    def student_percent(self):
        my_events = StudentEvent.objects.filter(student_id=self.student_id)
        events = my_events.count()
        attended = my_events.filter(attended=True).count()
        try:
            return attended/events
        except:
            return 1.0
    
    @property
    def student_percent_string(self):
        my_events = StudentEvent.objects.filter(student_id=self.student_id)
        events = my_events.count()
        attended = my_events.filter(attended=True).count()
        try:
            return "{}% ({} of {})".format(attended/events*100, attended, events)
        except:
            return "no listed events for this student"

    def __str__(self):
        return " - ".join([self.student_name, self.student_id, self.student_percent_string])

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id','student_courses']
        
class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_name', 'student_id', 'student_percent', 'student_percent_string', 'student_phone', 'student_email', 'student_courses']

class StudentEvent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    attended = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)

    def __str__(self):
        return " - ".join([self.event.event_title, self.student.student_name])

class StudentEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = ['student', 'event', 'attended', 'manual']

class StudentEventViewSet(viewsets.ModelViewSet):
    queryset = StudentEvent.objects.none()
    serializer_class = StudentEventSerializer

class RollCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvent
        fields = ['student_id', 'event', 'attended', 'manual']

class RollCallViewSet(viewsets.ModelViewSet):
    queryset = StudentEvent.objects.all()
    serializer_class = RollCallSerializer

class Config(models.Model):
    starting_date = models.DateField(default=date.today())
    ending_date = models.DateField(default=date.today()+timedelta(weeks=12))

    # By overriding these methods config becomes a singleton.
    def save(self, *args, **kwargs):
        self.pk = 1
        super(Config, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
