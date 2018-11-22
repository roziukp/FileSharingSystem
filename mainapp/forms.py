from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['']


class FilesForm(forms.ModelForm):
    class Meta:
        model = models.Files
        exclude = ['user']
