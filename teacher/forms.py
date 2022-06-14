from dataclasses import fields
import email
from django import forms
from .models import TeacherInfo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class TeacherForm(forms.ModelForm):
    
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
        'password': forms.PasswordInput()
        }

class TeacherInfoForm(forms.ModelForm):
    
    
    class Meta():

        model = TeacherInfo
        fields = ['mobile','branch']