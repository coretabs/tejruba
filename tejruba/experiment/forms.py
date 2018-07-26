from django import forms
from .models import Experiment, Profile
from django.contrib.auth.models import User

class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['content']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'birth_date')