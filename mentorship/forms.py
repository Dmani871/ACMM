from django import forms
from django.utils.html import format_html
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

    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)
    tcs_check = forms.BooleanField(required=True, label=format_html(
        '''I have read and agree to the <a href="{}">Privacy Policy</a> ''', '/mentorship/privacy/'))

    class Meta:
        model = models.MentorProfile
        exclude = ['is_active', 'date_joined']
        labels = {
            'year_applied': 'Qualification level prior to studying Medicine/Dentistry',
            'hear_about_us': 'How did you hear about us?'
        }
        help_texts = {
            'email': 'Email to be contacted regarding mentorship.',
            'work_email': 'Email to verify work/study status.'
        }


class MentorQualificationForm(forms.ModelForm):
    class Meta:
        model = models.MentorQualification
        exclude = ['profile']


class MenteeForm(forms.ModelForm):
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.SPECIALTY_CHOICES,
        label="What do you need help with?")

    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.ENTRANCE_EXAM_CHOICES,
        label="What entrance exam experience have you had?",
        required=False)

    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.INTERVIEW_EXPERIENCE_CHOICES,
        label="What interview experience have you had?",
        required=False)

    current_application = forms.ChoiceField(
        choices=models.TRUE_FALSE_CHOICES,
        label="Are you applying this year?",
        help_text="Our mentor scheme is for students applying to Medicine/Dentistry this year only"
    )

    mentor_need = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '5',
        'cols': '90',
        'maxlength': '500',
    }),
        label="Why do you want a mentor and what do you hope to gain ?",
        help_text="Max 500 Characters")

    mentor_help = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '5',
        'cols': '90',
        'maxlength': '500',
    }),
        label="How will a mentor help with your application?",
        help_text="Max 500 Characters")

    mentor_relationship = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '5',
        'cols': '90',
        'maxlength': '500',
    }),
        label="How will you go about fostering a good relationship your mentor?",
        help_text="Max 500 Characters")

    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)
    tcs_check = forms.BooleanField(required=True, label=format_html(
        '''I have read and agree to the <a href="{}">Privacy Policy</a> ''', '/mentorship/privacy'))

    class Meta:
        model = models.MenteeProfile
        exclude = ['date_joined', 'assigned_mentor', 'accepted']
        labels = {
            'year_applied': 'What is your current education level?',
            'hear_about_us': 'How did you hear about us?'
        }


class MenteeQualificationForm(forms.ModelForm):
    predicted = forms.ChoiceField(choices=models.TRUE_FALSE_CHOICES, required=True, label="Predicted ?")

    class Meta:
        model = models.MenteeQualification
        exclude = ['profile']


# TODO:Add tests
MenteeQualificationFormSet = forms.inlineformset_factory(
    models.MenteeProfile,
    model=models.MenteeQualification,
    form=MenteeQualificationForm,
    extra=2,
    min_num=1,
    max_num=10,
    validate_min=True,
    validate_max=True)

MentorQualificationFormSet = forms.inlineformset_factory(
    models.MentorProfile,
    model=models.MentorQualification,
    form=MentorQualificationForm,
    extra=2,
    min_num=1,
    max_num=10,
    validate_min=True,
    validate_max=True)
