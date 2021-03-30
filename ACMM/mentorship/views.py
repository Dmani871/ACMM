from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MentorForm,MentorQualificationFormSet
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