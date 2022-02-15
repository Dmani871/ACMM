from django import forms
from . import models


class MentorForm(forms.ModelForm):
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.SPECIALTY_CHOICES,
        label="What area can you provide support in?")
    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.INTERVIEW_EXPERIENCE_CHOICES,
        label="What interview experience do you have?")
    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=models.ENTRANCE_EXAM_CHOICES,
        label="What exam experience do you have?",
        required=False)

    class Meta:
        model = models.MentorProfile
        exclude = ['is_active', 'date_joined']
        labels = {
            'year_applied': 'Qualification level prior to studying Medicine/Dentistry',
            'hear_about_us': 'How did you hear about us?'
        }


class MentorQualificationForm(forms.ModelForm):
    class Meta:
        model = models.MentorQualification
        exclude = ['profile']


class MenteeForm(forms.ModelForm):
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.SPECIALTY_CHOICES)

    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.ENTRANCE_EXAM_CHOICES)

    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.INTERVIEW_EXPERIENCE_CHOICES)

    current_application = forms.ChoiceField(
        choices=models.TRUE_FALSE_CHOICES
    )

    mentor_need = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '5',
        'cols': '90',
        'maxlength': '500',
    }))
    mentor_help = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '5',
        'cols': '90',
        'maxlength': '500',
    }))

    mentor_relationship = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '5',
        'cols': '90',
        'maxlength': '500',
    }))

    class Meta:
        model = models.MenteeProfile
        exclude = ['date_joined', 'assigned_mentor', 'accepted']
        labels = {
            'year_applied': 'What is your current education level?',
            'hear_about_us': 'How did you hear about us?'
        }
