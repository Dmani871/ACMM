from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from encrypted_fields.fields import EncryptedEmailField, EncryptedCharField

ENTRANCE_EXAMS_TYPES = ("BMAT", "UCAT", "GAMSAT")
ENTRANCE_EXAM_CHOICES = list(zip(ENTRANCE_EXAMS_TYPES, ENTRANCE_EXAMS_TYPES))

INTERVIEW_EXPERIENCE_CHOICES = [("P", "Panel"), ("M", "MMI"), ("G", "Group")]

SPECIALTY_CHOICES = [
    ("PS", "Personal Statement"),
    ("I", "Interview"),
    ("EE", "Entrance Exam"),
    ("WE", "Work Experience"),
]

HEAR_ABOUT_US_CHOICES = [
    ("WM", "Word of mouth"),
    ("C", "Contact from ACMM team"),
    ("SM", "Social Media"),
    ("SU", "School/University"),
    ("E", "Employer"),
]
YEAR_APPLIED_CHOICES = [
    ("A2", "A level/IB"),
    ("GRAD", "Graduate"),
    ("OTHER", "Other"),
]

TRUE_FALSE_CHOICES = [(True, "Yes"), (False, "No")]


class CommonProfileInfo(models.Model):
    """Common profile info for all applicants."""

    # Personal Info
    personal_email = EncryptedEmailField(max_length=254)
    first_name = EncryptedCharField(max_length=30)
    last_name = EncryptedCharField(max_length=130)
    number = EncryptedCharField(max_length=130)

    # Application Data
    year_applied = models.CharField(max_length=10, choices=YEAR_APPLIED_CHOICES)

    entrance_exam_experience = ArrayField(
        models.CharField(max_length=10, choices=ENTRANCE_EXAM_CHOICES), default=list
    )
    interview_experience = ArrayField(
        models.CharField(max_length=10, choices=INTERVIEW_EXPERIENCE_CHOICES)
    )
    area_of_support = ArrayField(
        models.CharField(max_length=10, choices=SPECIALTY_CHOICES), default=list
    )
    wp_scheme = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    applied_before = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)

    # Consent
    contact_consent = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    sign_up_consent = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)

    # Metadata
    date_joined = models.DateTimeField(default=timezone.now)
    hear_about_us = models.CharField(
        max_length=10, choices=HEAR_ABOUT_US_CHOICES, default=None
    )

    class Meta:
        abstract = True
