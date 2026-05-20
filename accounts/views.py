from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from tutors.models import TutorProfile, Subject
from bookings.models import Booking

def parents_view(request):
    return render(request, 'accounts/parents.html')

def home_view(request):
    featured_tutors = TutorProfile.objects.order_by('-rating')[:3]
    tutor_count = TutorProfile.objects.count()
    subject_count = Subject.objects.count()
    booking_count = Booking.objects.filter(status='completed').count()
    subjects = Subject.objects.all()[:8]   # ← add this
    return render(request, 'home.html', {
        'featured_tutors': featured_tutors,
        'tutor_count': tutor_count,
        'subject_count': subject_count,
        'booking_count': booking_count,
        'subjects': subjects,             # ← add this
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'tutor':
                TutorProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    from bookings.models import Booking
    from tutors.models import TutorProfile

    if request.user.is_student():
        total = Booking.objects.filter(student=request.user).count()
        confirmed = Booking.objects.filter(student=request.user, status='confirmed').count()
        completed = Booking.objects.filter(student=request.user, status='completed').count()
        pending = Booking.objects.filter(student=request.user, status='pending').count()
        reviewed = Booking.objects.filter(student=request.user, status='completed', review__isnull=False).count()

        return render(request, 'accounts/dashboard.html', {
            'total': total,
            'confirmed': confirmed,
            'completed': completed,
            'pending': pending,
            'reviewed': reviewed,
        })

    else:
        pending = Booking.objects.filter(tutor__user=request.user, status='pending').count()
        confirmed = Booking.objects.filter(tutor__user=request.user, status='confirmed').count()
        completed = Booking.objects.filter(tutor__user=request.user, status='completed').count()
        tutor_profile = TutorProfile.objects.get(user=request.user)

        return render(request, 'accounts/dashboard.html', {
            'pending': pending,
            'confirmed': confirmed,
            'completed': completed,
            'rating': tutor_profile.rating,
        })

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')