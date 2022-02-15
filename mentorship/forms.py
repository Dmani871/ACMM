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
