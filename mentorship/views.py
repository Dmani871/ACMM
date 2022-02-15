from django.shortcuts import render,redirect
from . import forms
from django.forms import formset_factory
def thank_you_view(request):
    return render(request,  'mentorship/thank_you.html',{'page_title':'Thank You'})

def next_year_view(request):
    return render(request,  'mentorship/next_year.html',{'page_title':'Apply Next Year'})

def mentor_signup_view(request):
    if request.method == "POST":
        form = forms.MentorForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['honeypot']:
                return redirect('mentorship:thank_you')
            profile=form.save(commit=False)
            formset = forms.MentorQualificationFormSet(request.POST, request.FILES,instance=profile)
            if formset.is_valid():
                form.save()
                formset.save()
                return redirect('mentorship:thank_you')
        else:
            formset = forms.MentorQualificationFormSet(request.POST, request.FILES)
    else:
        form = forms.MentorForm()
        formset = forms.MentorQualificationFormSet()
    return render(request,  'mentorship/mentor_signup.html', {'page_title':'Mentor Application',"form": form,"qualification_formset": formset})
