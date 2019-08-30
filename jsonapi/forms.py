from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import *

class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
