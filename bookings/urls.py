from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:tutor_pk>/', views.book_session, name='book_session'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('confirm/<int:pk>/', views.confirm_booking, name='confirm_booking'),
    path('complete/<int:pk>/', views.complete_booking, name='complete_booking'),
    path('review/<int:booking_pk>/', views.leave_review, name='leave_review'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]