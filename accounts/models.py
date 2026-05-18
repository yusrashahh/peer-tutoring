from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_tutor(self):
        return self.role == 'tutor'

    def is_student(self):
        return self.role == 'student'