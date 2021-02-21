from django.shortcuts import render
from django.contrib.auth import login, authenticate

from .forms import UserCreationForm, MenteeCreationForm

def mentee_signup_view(request):
    form = MenteeCreationForm(request.POST)
    if form.is_valid():
        form.save()
    return render(request, 'mentee_signup.html', {'form': form})

def mentor_signup_view(request):

    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.save()
        user.refresh_from_db()
        user.profile.interests=form.cleaned_data.get('interests')
        user.profile.location=form.cleaned_data.get('country')
        user.profile.year_of_study=form.cleaned_data.get('year_of_study')
        user.profile.specialty= form.cleaned_data.get('specialty')
        user.profile.occupation= form.cleaned_data.get('current_occupation')
        user.profile.hear_about_us=form.cleaned_data.get('hear_about_us')
        user.profile.entrance_exam_experience=form.cleaned_data.get('entrance_exam_experience')
        user.profile.interview_experience=form.cleaned_data.get('interview_experience')
        user.profile.year_applied=form.cleaned_data.get('year_applied')
        user.profile.save()
    return render(request, 'mentor_signup.html', {'form': form})