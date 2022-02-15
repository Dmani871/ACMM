from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

#TODO:Turn into env import
SEX_TYPES=("M","F","O")
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

class MentorProfile(models.Model):
    email=models.EmailField(max_length=150)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=150)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    year_applied = models.CharField(max_length=10, choices=YEAR_APPLIED_CHOICES)
    date_joined = models.DateTimeField(default=timezone.now)
    hear_about_us = models.CharField(max_length=10, choices=HEAR_ABOUT_US_CHOICES, default=None)
    entrance_exam_experience = ArrayField(models.CharField(max_length=10, choices=ENTRANCE_EXAM_CHOICES), default=list)
    interview_experience = ArrayField(models.CharField(max_length=10, choices=INTERVIEW_EXPERIENCE_CHOICES))
    area_of_support = ArrayField(models.CharField(max_length=10, choices=SPECIALTY_CHOICES), default=list)
    occupation = models.CharField(max_length=10,choices=OCCUPATION_CHOICES)
    is_active = models.BooleanField(default=True)
