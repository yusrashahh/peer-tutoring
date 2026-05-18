from django.contrib import admin
from .models import Booking, Review

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'tutor', 'session_date', 'status')
    list_filter = ('status',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'rating', 'created_at')