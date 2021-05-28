from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.urls import reverse
from encrypted_fields import fields
from ACMM.settings.base import HASH_KEY

SEX_TYPES=("M","F")
SEX_CHOICES = list(zip(SEX_TYPES,SEX_TYPES))
ENTRANCE_EXAMS_TYPES=('BMAT','UCAT','GAMSAT')
ENTRANCE_EXAM_CHOICES = list(zip(ENTRANCE_EXAMS_TYPES,ENTRANCE_EXAMS_TYPES))
INTERVIEW_EXPERIENCE_CHOICES = [
    ("P", 'Panel'),
    ("M", 'MMI'),
    ('G', 'Group')
]
SPECIALTY_CHOICES = [
    ("PS", 'Personal Statement'),
    ("I", 'Interview'),
    ('EE', 'Entrance Exam'),
    ("WE", 'Work Experience')
]
HEAR_ABOUT_US_CHOICES = [
    ("WM", 'Word of mouth'),
    ("C", 'Contact from ACMM team'),
    ('SM', 'Social Media'),
    ('SU', 'School/University'),
    ("O", 'Other')
]

YEAR_APPLIED_CHOICES = [
    ('A2', 'A level/IB'),
    ('GRAD', 'Graduate')
]
EDUCATION_LEVEL_CHOICES = [
    ("A2", 'A Level'),
    ("AS", 'A/S Level'),
    ('IB', 'International Baccalaureate'),
    ('SH','Scottish Highers and Advanced Highers'),
    ("UG", 'Undergraduate'),
    ("M", 'Masters'),
    ("D", 'Doctorate')

]
OCCUPATION_CHOICES = [
    ('MD', 'Doctor'),
    ('D', 'Dentist'),
    ('MS', 'Medical Student'),
    ('DS', 'Dental Student')
]
GRADES=("A*","A","B","C","D","E","F","1","2","3","4","5","6","7","1st","2:1","2:2","3rd")
GRADE_CHOICES = list(zip(GRADES,GRADES))
TRUE_FALSE_CHOICES = [
    (True, 'Yes'),
    (False, 'No')
]
COURSE_CHOICES = [
    ('M', 'Medicine'),
    ('D', 'Dentistry'),
]



class CommonProfileInfo(models.Model):
    _email_data = fields.EncryptedEmailField()
    email = fields.SearchField(hash_key=HASH_KEY, encrypted_field_name="_email_data",unique=True)
    _default_first_name= fields.EncryptedCharField(max_length=30)
    first_name = fields.SearchField(
        hash_key=HASH_KEY, encrypted_field_name="_default_first_name"
    )
    _default_last_name= fields.EncryptedCharField(max_length=130)
    last_name = fields.SearchField(
        hash_key=HASH_KEY, encrypted_field_name="_default_last_name"
    )
    _default_sex= fields.EncryptedCharField(max_length=1,choices = SEX_CHOICES)
    sex = fields.SearchField(
        hash_key=HASH_KEY, encrypted_field_name="_default_sex"
    )
    year_applied=models.CharField(max_length=10,choices=YEAR_APPLIED_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)
    hear_about_us = models.CharField(max_length=10,choices=HEAR_ABOUT_US_CHOICES,default=None)
    entrance_exam_experience = ArrayField(models.CharField(max_length=10,choices = ENTRANCE_EXAM_CHOICES),default=list)
    interview_experience = ArrayField(models.CharField(max_length=10,choices = INTERVIEW_EXPERIENCE_CHOICES))
    area_of_support = ArrayField(models.CharField(max_length=10,choices = SPECIALTY_CHOICES),default=list)
    
    class Meta:
        abstract = True

    def get_admin_url(self):
        return reverse("admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name), args=(self.id,))



class MentorProfile(CommonProfileInfo):
    occupation = models.CharField(max_length=10,choices=OCCUPATION_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self): 
        return self.occupation+"-"+self.email
 
    

class MenteeProfile(CommonProfileInfo):
    mentor_need=models.TextField(null=True, blank=True)
    mentor_help=models.TextField(null=True, blank=True)
    mentor_relationship=models.TextField(null=True, blank=True)
    course = models.CharField(max_length=10,choices=COURSE_CHOICES)
    current_application=models.BooleanField(default=True,choices=TRUE_FALSE_CHOICES)
    accepted=models.BooleanField(default=False,choices=TRUE_FALSE_CHOICES)
    mentor=models.ForeignKey(MentorProfile, on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self): 
        return self.course+"-"+self.email


class CommonQualificationInfo(models.Model):
    name = models.CharField(max_length=50)
    education_level= models.CharField(max_length=10,choices=EDUCATION_LEVEL_CHOICES)
    class Meta:
        abstract = True

    def __str__(self): 
        return self.name+"-"+self.education_level

class MenteeQualification(CommonQualificationInfo):
    grade=models.CharField(max_length=10 ,choices=GRADE_CHOICES)
    predicted=models.BooleanField(default=False,choices=TRUE_FALSE_CHOICES)
    profile=models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)


class MentorQualification(CommonQualificationInfo):
    profile=models.ForeignKey(MentorProfile, on_delete=models.CASCADE)

