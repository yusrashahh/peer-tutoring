from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Review
from tutors.models import TutorProfile
from django import forms

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['session_date', 'notes']
        widgets = {
            'session_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience with this tutor...'}),
        }

@login_required
def book_session(request, tutor_pk):
    tutor = get_object_or_404(TutorProfile, pk=tutor_pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.tutor = tutor
            booking.save()
            messages.success(request, 'Session booked successfully!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    return render(request, 'bookings/book_session.html', {
        'form': form,
        'tutor': tutor
    })

@login_required
def my_bookings(request):
    if request.user.is_student():
        bookings = Booking.objects.filter(student=request.user).order_by('-created_at')
    else:
        bookings = Booking.objects.filter(tutor__user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, 'Booking confirmed!')
    return redirect('my_bookings')

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    
    # Only student or tutor involved can cancel
    if request.user != booking.student and request.user != booking.tutor.user:
        messages.error(request, 'You are not allowed to cancel this booking!')
        return redirect('my_bookings')
    
    # Only pending or confirmed bookings can be cancelled
    if booking.status in ['completed', 'cancelled']:
        messages.error(request, 'This booking cannot be cancelled!')
        return redirect('my_bookings')
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        booking.status = 'cancelled'
        booking.notes = f"Cancelled: {reason}" if reason else "Cancelled"
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('my_bookings')
    
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})

@login_required
def complete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'completed'
    booking.save()
    messages.success(request, 'Session marked as completed!')
    return redirect('my_bookings')

@login_required
def leave_review(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, student=request.user)
    if booking.status != 'completed':
        messages.error(request, 'You can only review completed sessions!')
        return redirect('my_bookings')
    if hasattr(booking, 'review'):
        messages.info(request, 'You have already reviewed this session!')
        return redirect('my_bookings')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            # Update tutor average rating
            tutor = booking.tutor
            reviews = Review.objects.filter(booking__tutor=tutor)
            tutor.rating = sum(r.rating for r in reviews) / reviews.count()
            tutor.save()
            messages.success(request, 'Review submitted! Thank you ⭐')
            return redirect('tutor_detail', pk=tutor.pk)
    else:
        form = ReviewForm()
    return render(request, 'bookings/review_form.html', {
        'form': form,
        'booking': booking
    })