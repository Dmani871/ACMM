from django.shortcuts import render
from django.shortcuts import redirect
from .forms import MentorForm,QualificationFormSet
from django.forms import formset_factory
from django.views.generic import TemplateView

#https://engineertodeveloper.com/getting-started-with-formsets-create-a-recipe-app/
#https://engineertodeveloper.com/dynamic-formsets-with-django/
def mentor_signup_view(request):
    form = MentorForm(request.POST)
    if request.method == 'POST':
        formset = QualificationFormSet(request.POST, request.FILES)
        if formset.is_valid():
            # do something with the formset.cleaned_data
            pass
    else:
        formset = QualificationFormSet()
    if form.is_valid():
        form.save()
    return render(request, 'mentor_signup.html', {'form': form,'qualification_formset': formset})


def manage_qualification(request):
    
    return render(request, 'a.html', {'qualification_formset': formset})