from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from cbc_system import settings


class Courses(models.Model):
    title = models.CharField(max_length=2550)
    acceptable_grade = models.CharField(max_length=2550)
    short_description = models.CharField(max_length=2550)



def __str__(self):
    return self.user


