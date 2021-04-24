from django import forms
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification,SPECIALTY_CHOICES,INTERVIEW_EXPERIENCE_CHOICES,ENTRANCE_EXAM_CHOICES
from django.forms import inlineformset_factory

TRUE_FALSE_CHOICES = [
    (True, 'Yes'),
    (False, 'No')
]
class MentorForm(forms.ModelForm):
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=SPECIALTY_CHOICES,
        label="What area can you provide support in?")   
    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INTERVIEW_EXPERIENCE_CHOICES,
        label="What interview experience do you have?")
    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=ENTRANCE_EXAM_CHOICES,
        label="What exam experience do you have?")
    class Meta:
        model = MentorProfile
        exclude=('is_active','date_joined')
        labels = {
            'year_applied':'Qualification level prior to studying Medicine/Dentistry',
            'hear_about_us':'How did you hear about us?'
        }
           
class MentorQualificationForm(forms.ModelForm):
    class Meta:
        model = MentorQualification
        exclude = ('profile',)

MentorQualificationFormSet = forms.inlineformset_factory(MentorProfile,model = MentorQualification, form=MentorQualificationForm,extra=1)


class MenteeForm(forms.ModelForm):    
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=SPECIALTY_CHOICES,
        label="What do you need help with?")   
    
    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=ENTRANCE_EXAM_CHOICES,
        label="What entrance exam experience have you had?")
    
    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=INTERVIEW_EXPERIENCE_CHOICES,
        label="What interview exam experience have you had?")
    
    current_application=forms.ChoiceField(
        choices = TRUE_FALSE_CHOICES,
        label="Are you applying this year?",
        help_text="Our mentor scheme is for students applying to Medicine in 2021 only"
        ) 
    
    mentor_need = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '5',
                'cols': '90',
                'maxlength': '500',
            }),
            required=True ,
            label="Why do you want a mentor and what do you hope to gain ?",
            help_text="Max 500 Charecters")
  
    mentor_help = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '5',
                'cols': '90',
                'maxlength': '500',
            }),
            required=True ,
            label="How will a mentor help with your application?",
            help_text="Max 500 Charecters")
    
    mentor_relationship = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '5',
                'cols': '90',
                'maxlength': '500',
            }),
            required=True ,
            label="How will you go about fostering a good relationship your mentor?",
            help_text="Max 500 Charecters")
    
    class Meta:
        model = MenteeProfile
        exclude=('date_joined','assigned_mentor')
        labels = {
            'year_applied':'What is your current education level?',
            'hear_about_us':'How did you hear about us?'
        }

        
class MenteeQualificationForm(forms.ModelForm):
    predicted=forms.ChoiceField(choices = TRUE_FALSE_CHOICES ,required=True ,label="Predicted ?") 
    class Meta:
        model = MenteeQualification
        exclude = ('profile',)

MenteeQualificationFormSet = forms.inlineformset_factory(MenteeProfile,model = MenteeQualification, form=MenteeQualificationForm,extra=1)




