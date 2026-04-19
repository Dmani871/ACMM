from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
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
    ("OT", "Other"),
]
YEAR_APPLIED_CHOICES = [
    ("A2", "A level/IB"),
    ("GRAD", "Graduate"),
    ("OT", "Other"),
]

TRUE_FALSE_CHOICES = [(True, "Yes"), (False, "No")]

COURSE_CHOICES = [
    ("M", "Medicine"),
    ("D", "Dentistry"),
]

EDUCATION_LEVEL_CHOICES = [
    ("A2", "A Level"),
    ("AS", "A/S Level"),
    ("IB", "International Baccalaureate"),
    ("SH", "Scottish Highers and Advanced Highers"),
    ("UG", "Undergraduate"),
    ("M", "Masters"),
    ("D", "Doctorate"),
]

GRADES = (
    "A*",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "1st",
    "2:1",
    "2:2",
    "3rd",
)
GRADE_CHOICES = list(zip(GRADES, GRADES))

OCCUPATION_CHOICES = [
    ("MD", "Doctor"),
    ("D", "Dentist"),
    ("MS", "Medical Student"),
    ("DS", "Dental Student"),
]


class CommonProfileInfo(models.Model):
    """Common profile info for all applicants."""

    # Personal Info
    personal_email = EncryptedEmailField(max_length=254)
    work_email = EncryptedEmailField(max_length=254)
    first_name = EncryptedCharField(max_length=30)
    last_name = EncryptedCharField(max_length=130)
    number = EncryptedCharField(max_length=130)

    # Application Data
    year_applied = models.CharField(max_length=5, choices=YEAR_APPLIED_CHOICES)

    entrance_exam_experience = ArrayField(
        models.CharField(max_length=10, choices=ENTRANCE_EXAM_CHOICES)
    )
    interview_experience = ArrayField(
        models.CharField(max_length=1, choices=INTERVIEW_EXPERIENCE_CHOICES)
    )
    area_of_support = ArrayField(
        models.CharField(max_length=2, choices=SPECIALTY_CHOICES)
    )
    wp_scheme = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    applied_before = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)

    # Consent
    contact_consent = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    tcs_consent = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)

    # Metadata
    date_joined = models.DateTimeField(default=timezone.now)
    hear_about_us = models.CharField(
        max_length=2, choices=HEAR_ABOUT_US_CHOICES, default=None
    )

    def get_admin_url(self):
        return reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=(self.id,),
        )

    class Meta:
        abstract = True


class MentorProfile(CommonProfileInfo):
    """Profile info for mentor applicants."""

    occupation = models.CharField(max_length=2, choices=OCCUPATION_CHOICES)
    is_active = models.BooleanField(default=False)
    additional_info = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return f"{self.occupation}-{self.personal_email}"


class MenteeProfile(CommonProfileInfo):
    """Profile info for mentee applicants."""

    # Application Data
    mentor_need = models.TextField()
    mentor_help = models.TextField()
    mentor_relationship = models.TextField()
    course = models.CharField(max_length=1, choices=COURSE_CHOICES)

    current_application = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    accepted = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    commitment = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    state_educated = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    family_support = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)

    mentor = models.ForeignKey(
        MentorProfile, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.course}-{str(self.personal_email)}"


class MenteeQualification(models.Model):
    """Mentee type Qualifications model"""

    name = models.CharField(max_length=50)
    education_level = models.CharField(max_length=10, choices=EDUCATION_LEVEL_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)
    predicted = models.BooleanField(default=False, choices=TRUE_FALSE_CHOICES)
    profile = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.education_level}-{str(self.name)}"
