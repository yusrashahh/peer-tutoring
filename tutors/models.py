from django.db import models
from accounts.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    availability = models.TextField(blank=True)
    rating = models.FloatField(default=0.0)
    profile_pic = models.ImageField(upload_to='tutor_pics/', blank=True)
    subjects = models.ManyToManyField(Subject, through='TutorSubject')

    def __str__(self):
        return f"{self.user.username}'s Profile"

class TutorSubject(models.Model):
    tutor = models.ForeignKey(TutorProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tutor', 'subject')