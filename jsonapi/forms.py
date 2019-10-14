from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import *

class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save()
        student = Student.objects.create(
            student_user=user,
            student_name="Test",
            student_id="30333333",
            student_phone="0400000000",
            student_email="fake123@fake.com")
        return user
