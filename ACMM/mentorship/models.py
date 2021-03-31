from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone



class CommonProfileInfo(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    entrance_exam_experience=ArrayField(models.CharField(max_length=100, blank=True),blank = True,null = True)
    interview_experience=ArrayField(models.CharField(max_length=100, blank=True),blank = True,null = True)
    area_of_support = ArrayField(models.CharField(max_length=255),blank = True,null = True)
    year_applied=models.CharField(max_length=255,blank = True,null = True)
    sex = models.CharField(max_length=1)
    date_joined = models.DateTimeField(default=timezone.now)
    
    class Meta:
        abstract = True
class MentorProfile(CommonProfileInfo):
    occupation = models.CharField(max_length=255,blank = True,null = True)
    application_strength = models.CharField(max_length=255,blank = True,null = True)
    year_of_study = models.PositiveIntegerField(blank = True,null = True)
    is_active = models.BooleanField(default=True)
 
    def __str__(self): 
        return self.email
class MenteeProfile(CommonProfileInfo):
    mentor_need=models.TextField(null=True, blank=True)
    mentor_help=models.TextField(null=True, blank=True)
    mentor_relationship=models.TextField(null=True, blank=True)
    course = models.CharField(max_length=255,blank = True,null = True)
    current_application=models.BooleanField(default=True)
    assigned_mentor=models.OneToOneField(MentorProfile, on_delete=models.SET_NULL,null=True,blank=True)
    

    def __str__(self): 
        return self.email
class CommonQualificationInfo(models.Model):
    name = models.CharField(max_length=50)
    education_level= models.CharField(max_length=50)
    class Meta:
        abstract = True
class MenteeQualification(CommonQualificationInfo):
    grade=models.CharField(max_length=10)
    predicted=models.BooleanField(default=False)
    profile=models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
class MentorQualification(CommonQualificationInfo):
    profile=models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
