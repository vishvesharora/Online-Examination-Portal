from pickle import TRUE
from typing_extensions import Required
from django.db import models

from django.contrib.auth.models import User
# Create your models here.

BRANCH_CHOICES= [
    ('CSE', 'Computer Science Eng'),
    ('ECE', 'Electrical Eng'),
    ('CE', 'Civil Eng'),
    ('ME', 'Mechanical Eng'),
    ]

class TeacherInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.IntegerField(null=True)
    branch = models.CharField(max_length=3, choices=BRANCH_CHOICES)
    #picture = models.ImageField(upload_to = 'student_profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    
    def get_instance(self):
        return self
    
    class Meta:
        verbose_name_plural = 'Teacher Info'