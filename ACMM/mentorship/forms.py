from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import MentorProfile


# options
SPECIALTY_CHOICES= [
    ('Personal Statement', 'Personal Statement'),
    ('Interview', 'Interview'),
    ('Entrance Exam', 'Entrance Exam'),
    ('Work Experience', 'Work Experience'),
    ('Choosing a University', 'Choosing a University ')]
APPLICATION_STAGES=SPECIALTY_CHOICES[:-2]   
INTERVIEW_EXPERIENCE_CHOICES = [
    ('Panel', 'Panel'),
    ('MMI', 'MMI'),
    ('Group', 'Group')]
YEAR_APPLIED_CHOICES = [
    ('A level', 'A level'),
    ('International Baccalaureate', 'International Baccalaureate'),
    ('Graduate', 'Graduate')]
ENTRANCE_EXAM_CHOICES = [
    ('BMAT', 'BMAT'),
    ('UKCAT', 'UKCAT'),
    ('GAMSAT', 'GAMSAT')]
OCCUPATION_CHOICES = [
    ('Doctor', 'Doctor'),
    ('Dentist', 'Dentist'),
    ('Medical Student', 'Medical Student'),
    ('Graduate Medical Student', 'Graduate Medical Student'),
    ('Medical Student Studying Abroad', 'Medical Student Studying Abroad'),
    ('Dental student', 'Dental student')]
INTREST_CHOICES = [
    ('Outreach Programmes', 'Outreach Programmes'),
    ('Speaking at events', 'Speaking at events'),
    ('Support for events', 'Support for events'),
    ('Provision of work experience/volunteering opportunities', 'Provision of work experience/volunteering opportunities'),
    ('Additional guidance for mentors (one off)', 'Additional guidance for mentors (one off)')]
HEAR_ABOUT_US_CHOICES = [
    ('Word of mouth', 'Word of mouth'),
    ('Contact from ACMM team', 'Contact from ACMM team'),
    ('Social Media', 'Social Media'),
    ('Other','Other')]
COURSE_CHOICES =[
    ('Medicine', 'Medicine'),
    ('Dentistry', 'Dentistry'),
    ('Graduate Medicine', 'Graduate Medicine'),
]


class MentorCreationForm(forms.ModelForm):
    current_occupation=forms.ChoiceField(choices = OCCUPATION_CHOICES,required=True) 
    interests=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTREST_CHOICES,label="Areas of Interests:")
    specialty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=SPECIALTY_CHOICES,label="Position/Specialty:")   
    application_strength= forms.ChoiceField(choices=APPLICATION_STAGES,label="What was your strength in the application?")                            
    hear_about_us = forms.ChoiceField(widget=forms.RadioSelect, choices=HEAR_ABOUT_US_CHOICES ,label="Hear about us?")                       
    year_of_study = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],required=False, help_text='For Students')
    entrance_exam_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ENTRANCE_EXAM_CHOICES,label="Entrance Exam Experience:")
    interview_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTERVIEW_EXPERIENCE_CHOICES,label="Interview Experience:")
    year_applied = forms.ChoiceField(widget=forms.RadioSelect,
                                          choices=YEAR_APPLIED_CHOICES,label="Year Applied:")
    class Meta:
        model = MentorProfile
        fields = ('first_name','last_name','email',)

    def save(self, commit=True):
        
        # Save the provided password in hashed format
        profile = super().save(commit=False)
        print(profile)
        if commit:
            profile.save()
        return profile