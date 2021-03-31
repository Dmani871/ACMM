from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MentorForm,MenteeForm,MentorQualificationFormSet,MenteeQualificationFormSet
from django.forms import formset_factory
from django.views.generic import TemplateView

def mentor_signup_view(request):
    if request.method == "POST":
        form = MentorForm(request.POST)
        if form.is_valid():
            profile=form.save(commit=False)
            formset = MentorQualificationFormSet(request.POST, request.FILES,instance=profile)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('/thanks')
        formset = MentorQualificationFormSet(request.POST, request.FILES)
        return render(request,  'mentor_signup.html', {"form": form,"qualification_formset": formset})
    else:
        form = MentorForm()
        formset = MentorQualificationFormSet()
        return render(request,  'mentor_signup.html', {"form": form,"qualification_formset": formset})

def mentee_signup_view(request):
    if request.method == "POST":
        form = MenteeForm(request.POST)
       
        if form.is_valid():
            if form.cleaned_data['current_application']=="False":
                return redirect('/nextyear')
            profile=form.save(commit=False)
            formset = MenteeQualificationFormSet(request.POST, request.FILES,instance=profile)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('/thanks')
        formset = MenteeQualificationFormSet(request.POST, request.FILES)
        return render(request,  'mentee_signup.html', {"form": form,"qualification_formset": formset})
    else:
        form = MenteeForm()
        formset = MenteeQualificationFormSet()
        return render(request,  'mentee_signup.html', {"form": form,"qualification_formset": formset})

def thank_you_view(request):
    return render(request,  'thank_you.html')

def next_year_view(request):
    return render(request,  'next_year.html')

def applications_view(request):
    return render(request,  'applications.html')