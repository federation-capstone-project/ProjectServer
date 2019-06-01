from django.db import models

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

class Student(models.Model):
    student_name = models.CharField(max_length=200)
    student_id = models.CharField(max_length=200)

class Clinician(models.Model):
    clinician_name = models.CharField(max_length=200)
    staff_id = models.CharField(max_length=200)
    staff_mac_address = models.CharField(max_length=200)
