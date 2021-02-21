from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import User
from django_countries import countries
COUNTRY_CHOICES = tuple(countries)

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
class UserCreationForm(forms.ModelForm):
    current_occupation=forms.ChoiceField(choices = OCCUPATION_CHOICES,required=True) 
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, required=True ,label="Location:")
    interests=forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTREST_CHOICES,label="Areas of Interests:")
    specialty=forms.CharField(max_length=30, required=True,label="Position/Speciality:")                             
    hear_about_us= forms.ChoiceField(widget=forms.RadioSelect, choices=HEAR_ABOUT_US_CHOICES ,label="Hear about us?")                       
    year_of_study = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],required=False, help_text='For Students')
    class Meta:
        model = User
        fields = ('first_name','last_name','email',)

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
