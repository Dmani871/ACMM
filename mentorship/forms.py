from django import forms
from . import models


class MentorForm(forms.ModelForm):
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.SPECIALTY_CHOICES)
    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.INTERVIEW_EXPERIENCE_CHOICES)
    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=models.ENTRANCE_EXAM_CHOICES)
    class Meta:
        model = models.MentorProfile
        exclude = ['is_active','date_joined']

