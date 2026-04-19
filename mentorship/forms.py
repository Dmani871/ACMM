from email.policy import default

from django import forms
from django.utils.html import format_html

from . import models

LABELS = {
    "year_applied": "Qualification level prior to studying Medicine/Dentistry",
    "hear_about_us": "How did you hear about us?",
    "number": "Contact Number",
    "contact_consent": "Do you consent to being added to ACMM group chat?",
    "commitment": "Are you able to commit to monthly meetings with your mentor throughout the year of the mentoring programme?",
    "state_educated": "Do you attend a state school?",
    "family_support": "Do you have a parent(s) who are doctors?",
    "wp_scheme": "Are you applying via a widening participation (WP) scheme?",
    "applied_before": "Have you applied before?",
}


class MentorForm(forms.ModelForm):
    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.SPECIALTY_CHOICES,
        label="What area can you provide support in?",
    )
    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.INTERVIEW_EXPERIENCE_CHOICES,
        label="What interview experience do you have?",
    )
    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(),
        choices=models.ENTRANCE_EXAM_CHOICES,
        label="What exam experience do you have?",
        required=False,
    )
    additional_info = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "2",
                "cols": "90",
                "maxlength": "500",
            }
        ),
        label="Any additional comments?",
        help_text="Max 500 Characters",
        required=False,
    )
    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)
    tcs_consent = forms.BooleanField(
        required=True,
        label=format_html(
            """I have read and agree to the <a href="{}">Privacy Policy</a> """,
            "/mentorship/privacy",
        ),
    )

    class Meta:
        model = models.MentorProfile
        exclude = ["is_active", "date_joined"]
        labels = {
            **LABELS,
            "wp_scheme": "Did you apply via a widening participation (WP) scheme?",
            "applied_before": "Did you apply multiple times before being accepted on a course?",
        }
        help_texts = {
            "work_email": "Email to verify work/study status (NHS or University email).",
            "wp_scheme": "Useful for matching you with a mentee who is part of a WP scheme.",
            "applied_before": "Useful for matching you with a mentee who had a similar experience.",
        }


class MenteeForm(forms.ModelForm):

    area_of_support = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.SPECIALTY_CHOICES,
        label="What do you need help with?",
    )

    entrance_exam_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.ENTRANCE_EXAM_CHOICES,
        label="What entrance exam experience have you had?",
        required=False,
    )

    interview_experience = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=models.INTERVIEW_EXPERIENCE_CHOICES,
        label="What interview experience have you had?",
        required=False,
    )

    current_application = forms.ChoiceField(
        choices=models.TRUE_FALSE_CHOICES,
        label="Are you applying this year?",
        help_text="Our mentor scheme is for students applying to Medicine/Dentistry this year only",
    )

    mentor_need = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "5",
                "cols": "90",
                "maxlength": "500",
            }
        ),
        label="Why do you want a mentor and what do you hope to gain ?",
        help_text="Max 500 Characters",
    )

    mentor_help = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "5",
                "cols": "90",
                "maxlength": "500",
            }
        ),
        label="How will a mentor help with your application?",
        help_text="Max 500 Characters",
    )

    mentor_relationship = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": "5",
                "cols": "90",
                "maxlength": "500",
            }
        ),
        label="How will you go about fostering a good relationship your mentor?",
        help_text="Max 500 Characters",
    )

    honeypot = forms.CharField(widget=forms.HiddenInput(), required=False)
    tcs_consent = forms.BooleanField(
        required=True,
        label=format_html(
            """I have read and agree to the <a href="{}">Privacy Policy</a> """,
            "/mentorship/privacy",
        ),
    )

    class Meta:
        model = models.MenteeProfile
        exclude = ["date_joined", "assigned_mentor", "accepted"]
        labels = {
            **LABELS,
            "year_applied": "What is your current education level?",
        }


class MenteeQualificationForm(forms.ModelForm):
    predicted = forms.ChoiceField(
        choices=models.TRUE_FALSE_CHOICES, required=True, label="Predicted ?"
    )

    class Meta:
        model = models.MenteeQualification
        exclude = ["profile"]


MenteeQualificationFormSet = forms.inlineformset_factory(
    models.MenteeProfile,
    model=models.MenteeQualification,
    form=MenteeQualificationForm,
    extra=2,
    min_num=1,
    max_num=10,
    validate_min=True,
    validate_max=True,
)
