from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import User,MenteeProfile
from django_countries import countries
COUNTRY_CHOICES = tuple(countries)
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
class UserCreationForm(forms.ModelForm):
    current_occupation=forms.ChoiceField(choices = OCCUPATION_CHOICES,required=True) 
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True ,label="Location:")
    interests=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTREST_CHOICES,label="Areas of Interests:")
    specialty=forms.CharField(max_length=30, required=True,label="Position/Speciality:")                             
    hear_about_us= forms.ChoiceField(widget=forms.RadioSelect, choices=HEAR_ABOUT_US_CHOICES ,label="Hear about us?")                       
    year_of_study = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],required=False, help_text='For Students')
    entrance_exam_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ENTRANCE_EXAM_CHOICES,label="Entrance Exam Experience:")
    interview_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTERVIEW_EXPERIENCE_CHOICES,label="Interview Experience:")
    year_applied = forms.ChoiceField(widget=forms.RadioSelect,
                                          choices=YEAR_APPLIED_CHOICES,label="Year Applied:")
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class MenteeCreationForm(forms.ModelForm):
    applied_this_year = forms.ChoiceField(widget=forms.RadioSelect, choices=((False, 'No'), (True, 'Yes')) ,required=True,label="Have you applied to medicine or dentistry this year?")       
    course = forms.ChoiceField(widget=forms.RadioSelect,required=True,choices=COURSE_CHOICES,label="Which course have you applied to?")       
    help_needed=forms.CharField(max_length=255, required=True,label="What aspects of the interview do you feel you need support with?") 
    preparation=forms.CharField(widget=forms.Textarea,required=True,label="How have/will you be preparing for your Medicine/Dentistry interview?")       
    confidence = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],required=True, label="How confident do you feel for your Medicine/Dentistry interview? ",help_text='1 being the least and 10 being the most')
    entrance_exam = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ENTRANCE_EXAM_CHOICES,label="What Entry Exam are you sitting?")
    class Meta:
        model = MenteeProfile
        fields = ('first_name','last_name','email','entrance_exam','course','confidence','preparation','help_needed','applied_this_year')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
