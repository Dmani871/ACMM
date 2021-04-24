from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
SEX_TYPES=("M","F")
SEX_CHOICES = list(zip(SEX_TYPES,SEX_TYPES))
ENTRANCE_EXAMS_TYPES=('BMAT','UKCAT','GAMSAT')
ENTRANCE_EXAM_CHOICES = list(zip(ENTRANCE_EXAMS_TYPES,ENTRANCE_EXAMS_TYPES))
INTERVIEW_TYPES=('Panel','MMI','Group')
INTERVIEW_EXPERIENCE_CHOICES = list(zip(INTERVIEW_TYPES,INTERVIEW_TYPES))
SPECIALTIES=('Personal Statement','Interview','Entrance Exam','Work Experience')
SPECIALTY_CHOICES=list(zip(SPECIALTIES,SPECIALTIES))
APPLICATION_STAGES=SPECIALTY_CHOICES[:-2] 
HEAR_ABOUT_US_TYPES=('Word of mouth','Contact from ACMM team','Social Media','Other')
HEAR_ABOUT_US_CHOICES=list(zip(HEAR_ABOUT_US_TYPES,HEAR_ABOUT_US_TYPES))
YEAR_APPLIED_CHOICES = [
    ('A2', 'A level/IB'),
    ('GRAD', 'Graduate')
]
EDUCATION_LEVEL_CHOICES = [
    ("A2", 'A Level'),
    ("AS", 'A/S Level'),
    ('IB', 'International Baccalaureate'),
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
COURSES=('Medicine','Dentistry','Graduate Medicine')
COURSE_CHOICES =list(zip(COURSES,COURSES))


class CommonProfileInfo(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    sex = models.CharField(max_length=1,choices = SEX_CHOICES)
    year_applied=models.CharField(max_length=10,choices=YEAR_APPLIED_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)
    hear_about_us = models.CharField(max_length=50,choices=HEAR_ABOUT_US_CHOICES,default=None)
    entrance_exam_experience = ArrayField(models.CharField(max_length=10,choices = ENTRANCE_EXAM_CHOICES))
    interview_experience = ArrayField(models.CharField(max_length=10,choices = INTERVIEW_EXPERIENCE_CHOICES))
    area_of_support = ArrayField(models.CharField(max_length=10,choices = SPECIALTY_CHOICES),default=list)
    class Meta:
        abstract = True
class MentorProfile(CommonProfileInfo):
    occupation = models.CharField(max_length=10,choices=OCCUPATION_CHOICES)
    is_active = models.BooleanField(default=True)
 
    def __str__(self): 
        return self.email
class MenteeProfile(CommonProfileInfo):
    mentor_need=models.TextField(null=True, blank=True)
    mentor_help=models.TextField(null=True, blank=True)
    mentor_relationship=models.TextField(null=True, blank=True)
    course = models.CharField(max_length=10,choices=COURSE_CHOICES)
    current_application=models.BooleanField(default=True,choices=TRUE_FALSE_CHOICES)
    assigned_mentor=models.OneToOneField(MentorProfile, on_delete=models.SET_NULL,null=True,blank=True)
    

    def __str__(self): 
        return self.email
class CommonQualificationInfo(models.Model):
    name = models.CharField(max_length=50)
    education_level= models.CharField(max_length=10,choices=EDUCATION_LEVEL_CHOICES)
    class Meta:
        abstract = True
class MenteeQualification(CommonQualificationInfo):
    grade=models.CharField(max_length=10 ,choices=GRADE_CHOICES)
    predicted=models.BooleanField(default=False)
    profile=models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
class MentorQualification(CommonQualificationInfo):
    profile=models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
