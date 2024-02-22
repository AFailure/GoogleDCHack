# forms.py
from django import forms
from .models import User, Profile


class SurveyForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']


class ProfileSurveyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'image', 'verified']
