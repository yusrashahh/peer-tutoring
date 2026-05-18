from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TutorProfile, Subject
from .forms import TutorProfileForm, TutorSearchForm

def tutor_list(request):
    tutors = TutorProfile.objects.all()
    form = TutorSearchForm(request.GET)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        subject = form.cleaned_data.get('subject')
        max_rate = form.cleaned_data.get('max_rate')

        if query:
            tutors = tutors.filter(user__username__icontains=query)
        if subject:
            tutors = tutors.filter(subjects=subject)
        if max_rate:
            tutors = tutors.filter(hourly_rate__lte=max_rate)

    return render(request, 'tutors/tutor_list.html', {
        'tutors': tutors,
        'form': form
    })

def tutor_detail(request, pk):
    tutor = get_object_or_404(TutorProfile, pk=pk)
    return render(request, 'tutors/tutor_detail.html', {'tutor': tutor})

@login_required
def edit_tutor_profile(request):
    if not request.user.is_tutor():
        messages.error(request, 'Only tutors can access this page!')
        return redirect('dashboard')

    tutor_profile = get_object_or_404(TutorProfile, user=request.user)

    if request.method == 'POST':
        form = TutorProfileForm(request.POST, request.FILES, instance=tutor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = TutorProfileForm(instance=tutor_profile)

    return render(request, 'tutors/edit_profile.html', {'form': form})