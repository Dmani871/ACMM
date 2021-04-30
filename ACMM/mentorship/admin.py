from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification
from .forms import MentorForm,MenteeForm
from django.forms import formset_factory
from django.forms import inlineformset_factory
from collections import defaultdict
from django.urls import reverse
import numpy as np
import pandas as pd

from django.conf import settings
from django.core import mail

class MentorQualificationInline(admin.TabularInline):
    model = MentorQualification
    extra=0
    can_delete=True
class MenteeInline(admin.TabularInline):
    model = MenteeProfile
    extra=0
    can_delete=True


class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline,MenteeInline
    ]
    search_fields = ['first_name','last_name','email']
    list_filter = ['occupation','date_joined','is_active','sex','year_applied']
    exclude = [""]
    form = MentorForm
    list_display = ['first_name','last_name','email']

    fieldsets = [
        ('Personal Information',{'fields': ['first_name','last_name','email','sex']}),
        ('Background Information', {'fields': ['occupation','year_applied','entrance_exam_experience','interview_experience','area_of_support']}),
        ('Meta', {'fields': ['date_joined','hear_about_us','is_active']})
    ]

class MenteeQualificationInline(admin.TabularInline):
    model = MenteeQualification
    extra=0
    can_delete=True

class MenteeAdmin(admin.ModelAdmin):
    inlines = [
        MenteeQualificationInline,
    ]
    exclude = [""]
    form = MenteeForm
    search_fields = ['first_name','last_name','email']
    list_filter = ['course','date_joined','accepted','sex','year_applied']
    list_display = ['first_name','last_name','email','mentor']
    fieldsets = [
        ('Personal Information',{'fields': ['first_name','last_name','email','sex']}),
        ('Background Information', {'fields': ['year_applied','entrance_exam_experience','interview_experience','area_of_support']}),
        ('Application Information', {'fields': ['course','mentor_need','mentor_help','mentor_relationship','current_application','accepted']}),
        ('Mentor', {'fields': ['mentor']}),
        ('Meta', {'fields': ['date_joined','hear_about_us']})
    ]


    def generate_matches_messages(self,mentees):
        emails=[]
        subject='Congratulations! You have been matched!'
        body='We have found the perfect match.'
        for mentee in mentees:
            if mentee.mentor !=None:
                mentor=mentee.mentor
                mentee_email = mail.EmailMessage(subject=subject,body=body,to=[mentee.email])
                mentor_email = mail.EmailMessage(subject=subject,body=body,to=[mentor.email])
                emails.append(mentor_email)
                emails.append(mentee_email)
        return emails
   
    def email_matches(self, request, queryset):
        with mail.get_connection() as connection:
            messages=self.generate_matches_messages(queryset)
            connection.send_messages(messages)
  
    def assign_mentor(self, request, queryset):
        available_mentors = MentorProfile.objects.filter(is_active=True,menteeprofile__isnull=True)
        mentee_preferences=defaultdict(dict)
        mentor_preferences=defaultdict(list)
        for mentee in queryset:
            matches=defaultdict(dict)
            for mentor in available_mentors:
                ranking=0
                if mentee.course == mentor.occupation[0]:
                    ranking=10
                if mentor.year_applied==mentee.year_applied:
                    ranking *=2
                if mentor.sex!=mentee.sex:
                    ranking*=0.8
                
                support_factor = len(np.intersect1d(mentor.area_of_support,mentee.area_of_support))+1
                interview_factor = len(np.intersect1d(mentor.interview_experience,mentee.interview_experience))
                exam_factor = len(np.intersect1d(mentor.entrance_exam_experience,mentee.entrance_exam_experience))
                if 'EE' in mentee.area_of_support:
                    exam_factor *=2
                if 'I' in mentee.area_of_support:
                    interview_factor *=2
                mentee_qualifications=[q.name for q in MenteeQualification.objects.filter(profile=mentee)]
                mentor_qualifications=[q.name for q in MentorQualification.objects.filter(profile=mentor)]
                subject_factor = len(np.intersect1d(mentor_qualifications,mentee_qualifications))
                mentor_factor =1+((exam_factor+interview_factor+subject_factor)*0.1)
                ranking=(ranking*support_factor)*mentor_factor
                

                if ranking >0:
                    matches[mentor.id]=ranking
            mentee_preferences[mentee.id]=matches
        
        matches_df=pd.DataFrame(mentee_preferences)  
        matches=matches_df.idxmax(axis=1)
        for mentor_id,mentee_id in matches.items():
            mentee=MenteeProfile.objects.get(id=mentee_id)
            mentor=MentorProfile.objects.get(id=mentor_id)
            mentee.mentor=mentor
            mentee.save()


    assign_mentor.short_description = "Assign a mentor to each mentee"
    email_matches.short_description = "Email matches"
    actions = ["assign_mentor","email_matches"]


admin.site.register(MentorProfile,MentorAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)