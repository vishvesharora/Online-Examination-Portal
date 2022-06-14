from dataclasses import fields
import email
from django import forms
from .models import StudentInfo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class StudentForm(forms.ModelForm):
    
    
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
        'password': forms.PasswordInput()
        }

class StudentInfoForm(forms.ModelForm):
    
    
    class Meta():

        model = StudentInfo
        fields = ['mobile','branch']
        