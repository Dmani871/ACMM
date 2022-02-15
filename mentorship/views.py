from django.shortcuts import render, redirect
from . import forms


def thank_you_view(request):
    return render(request, 'mentorship/thank_you.html', {'page_title': 'Thank You'})


def next_year_view(request):
    return render(request, 'mentorship/next_year.html', {'page_title': 'Apply Next Year'})


def applications_view(request):
    return render(request, 'mentorship/applications.html', {'page_title': 'ACMM Application Portal'})


def mentor_signup_view(request):
    if request.method == "POST":
        form = forms.MentorForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            formset = forms.MentorQualificationFormSet(request.POST, request.FILES, instance=profile)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('mentorship:thank_you')
        else:
            formset = forms.MentorQualificationFormSet(request.POST, request.FILES)
    else:
        form = forms.MentorForm()
        formset = forms.MentorQualificationFormSet()
    return render(request, 'mentorship/mentor_signup.html',
                  {'page_title': 'Mentor Application', "form": form, "qualification_formset": formset})


def mentee_signup_view(request):
    if request.method == "POST":
        form = forms.MenteeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['current_application'] == "False":
                return redirect('mentorship:next_year')
            profile = form.save(commit=False)
            formset = forms.MenteeQualificationFormSet(request.POST, request.FILES, instance=profile)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('mentorship:thank_you')
        else:
            formset = forms.MenteeQualificationFormSet(request.POST, request.FILES)
    else:
        form = forms.MenteeForm()
        formset = forms.MenteeQualificationFormSet()
    return render(request, 'mentorship/mentee_signup.html',
                  {'page_title': 'Mentee Application', "form": form, "qualification_formset": formset})
