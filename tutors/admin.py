from django.contrib import admin
from .models import Subject, TutorProfile, TutorSubject

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')

@admin.register(TutorProfile)
class TutorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hourly_rate', 'rating')

@admin.register(TutorSubject)
class TutorSubjectAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'subject')