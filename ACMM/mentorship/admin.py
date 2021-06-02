import csv
from django.core import serializers
from django.core import mail
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.forms import formset_factory
from django.forms import inlineformset_factory
from django.urls import reverse
from django.utils.html import format_html
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification
from .forms import MentorForm,MenteeForm
from collections import defaultdict
import pandas as pd
import numpy as np
from collections import Counter


@admin.action(description='Export Selected Profiles')
def export_as_csv(self, request, queryset):
    meta = self.model._meta
    field_names = [field.name for field in meta.fields]
    column_names= field_names+["qualifications"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(column_names)
    for obj in queryset:
        row_contents=[getattr(obj, field) for field in field_names]
        if isinstance(obj, MenteeProfile):
            qualifications=[(q.name,q.education_level,q.grade,q.predicted) for q in MenteeQualification.objects.filter(profile=obj)]
        else:
            qualifications=[(q.name,q.education_level) for q in MentorQualification.objects.filter(profile=obj)]
        row_contents.append(qualifications)
        row = writer.writerow(row_contents)
    return response

class MentorQualificationInline(admin.TabularInline):
    model = MentorQualification
    extra=0
    can_delete=True

class MenteeInline(admin.StackedInline):
    model = MenteeProfile
    extra=0
    can_delete=False
    show_change_link=True
    form = MenteeForm
    fieldsets = [
        ('Mentee Personal Information',{'fields': ['first_name','last_name','email','sex']}),
        ('Mentee Background Information', {'fields': ['year_applied','entrance_exam_experience','interview_experience','area_of_support']}),
        ('Mentee Application Information', {'fields': ['course','mentor_need','mentor_help','mentor_relationship','current_application','accepted']}),
    ]

class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline,MenteeInline
    ]
    #search_fields = ['first_name','last_name','email']
    list_filter = ['occupation','date_joined','is_active','year_applied']
    exclude = [""]
    form = MentorForm
    list_display = ['email','first_name','last_name']

    fieldsets = [
        ('Personal Information',{'fields': ['first_name','last_name','email','sex']}),
        ('Background Information', {'fields': ['occupation','year_applied','entrance_exam_experience','interview_experience','area_of_support']}),
        ('Meta', {'fields': ['date_joined','hear_about_us','is_active']})
    ]

    @admin.action(description='Email Info Pack')
    def email_info_pack(self, request, queryset):
        with mail.get_connection() as connection:
            messages=[]
            for mentor in queryset:
                body=f"Hi {mentor.first_name},\nWe are so excited to welcome you to our coummnity of mentors.Please find the information pack attached below detailing our guidelines.\nKind regards\nACMM Team"
                email = mail.EmailMessage(
                    subject="Mentor Welcome Information",
                    body=body,
                    to=[mentor.email],
                    reply_to=["mentoring@acmedicalmentors.co.uk"]
                )
                email.attach_file('./static/mentorship/resources/Mentor_Sign_Up.pdf')
                messages.append(email)
            connection.send_messages(messages)

            
    actions = [export_as_csv,email_info_pack]

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
    #search_fields = ['first_name','last_name','email','entrance_exam_experience','interview_experience','area_of_support']
    list_filter = ['course','date_joined','accepted','year_applied','hear_about_us']
    list_display = ['email','first_name','last_name','mentor_link','entrance_exam_experience','interview_experience','area_of_support']
    fieldsets = [
        ('Personal Information',{'fields': ['first_name','last_name','email','sex']}),
        ('Background Information', {'fields': ['year_applied','entrance_exam_experience','interview_experience','area_of_support']}),
        ('Application Information', {'fields': ['course','mentor_need','mentor_help','mentor_relationship','current_application','accepted']}),
        ('Mentor', {'fields': ['mentor']}),
        ('Meta', {'fields': ['date_joined','hear_about_us']})
    ]
    def mentor_link(self, obj):
        mentor=obj.mentor
        if mentor:
            admin_url = mentor.get_admin_url()
            return format_html('<a href="{}">{}</a>', admin_url,mentor)
        else:
            return None
    mentor_link.short_description = 'Mentor'

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
   
    @admin.action(description='Email Matche(s)')
    def email_matches(self, request, queryset):
        with mail.get_connection() as connection:
            messages=self.generate_matches_messages(queryset)
            connection.send_messages(messages)
    @admin.action(description='Assign a mentor to each mentee')
    def assign_mentor(self, request, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        available_mentors = MentorProfile.objects.filter(is_active=True,menteeprofile__isnull=True)
        mentee_preferences=defaultdict(dict)
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
                    
                    support_factor = len(np.intersect1d(mentor.area_of_support,mentee.area_of_support))
                    interview_factor = len(np.intersect1d(mentor.interview_experience,mentee.interview_experience))
                    exam_factor = len(np.intersect1d(mentor.entrance_exam_experience,mentee.entrance_exam_experience))
                    
                    if ('EE' in mentee.area_of_support and exam_factor==0) or ('I' in mentee.area_of_support and interview_factor==0):
                        support_factor=0
                    if 'EE' in mentee.area_of_support:
                        exam_factor *=5
                    if 'I' in mentee.area_of_support:
                        interview_factor *=5
                    mentor_factor =1+((exam_factor+interview_factor)*0.1)
                    ranking=(ranking*support_factor)*mentor_factor
                    if ranking >0:
                        matches[mentor.id]=ranking
            mentee_preferences[mentee.id]=matches
        
        matches_df=pd.DataFrame(mentee_preferences)  
        mentor_list=matches_df.index.tolist()
        waiting_list = []
        no_matches=[]
        proposals = {}

        counter=0
        while len(waiting_list)<len(mentor_list) and counter<1000:
            for mentor in mentor_list:
                if mentor not in waiting_list:
                    best_choice = matches_df.loc[mentor].idxmax()
                    rank=matches_df.loc[mentor][best_choice]
                    if rank>0:
                        proposals[(mentor, best_choice)]=matches_df.loc[mentor][best_choice]   
                    else:
                        no_matches.append(mentor)
            overlays = Counter([key[1] for key in proposals.keys()])
            for mentee in overlays.keys():
                if overlays[mentee]>1:
                    pairs={pair: proposals[pair] for pair in proposals.keys() 
                            if mentee in pair}.items()
                    pairs_to_drop=sorted(pairs,key=lambda x: x[1])[:-1]
                    for p_to_drop in pairs_to_drop:
                        del proposals[p_to_drop[0]]
                        matches_df.at[p_to_drop[0][0],p_to_drop[0][1]]=0
            waiting_list = [pair[0] for pair in proposals.keys()]+no_matches
            counter+=1
       

        for pair in proposals.keys():
            mentor=MentorProfile.objects.get(id=pair[0])
            mentee=MenteeProfile.objects.get(id=pair[1])
            mentee.mentor=mentor
            LogEntry.objects.log_action(
                user_id=request.user.id, 
                content_type_id=ct.pk,
                object_id=mentee.pk,
                object_repr=mentee.__str__(),
                action_flag=CHANGE,
                change_message="Added mentor match") 
            mentee.save()
        l = LogEntry(user_id=request.user.id, action_flag=CHANGE,content_type_id=ct.pk, change_message="Mentee-Mentor matches ran")
        l.save()
        
    @admin.action(description='Export Matches Email')
    def export_matches(self, request, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        meta = self.model._meta
        column_names= ["mentee(s)","mentor(s)"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(column_names)
        for mentee in queryset:
            if mentee.mentor !=None:
                mentor=mentee.mentor
                row_contents=[mentee.email,mentor.email]
                row = writer.writerow(row_contents)
                LogEntry.objects.log_action(
                    user_id=request.user.id, 
                    content_type_id=ct.pk,
                    object_id=mentee.pk,
                    object_repr=mentee.__str__(),
                    action_flag=CHANGE,
                    change_message="Exported Profile") 
        return response

    @admin.action(description='Export Matches Info')
    def export_matches_info(self, request, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        meta = self.model._meta
        column_names= ["mentee.id","mentor.id",
                    "mentee.course","mentor.occupation",
                    "mentee.year_applied","mentor.year_applied",
                    "mentee.sex","mentor.sex",
                    "mentee.area_of_support","mentor.area_of_support",
                    "mentee.interview_experience","mentor.interview_experience",
                    "mentee.entrance_exam_experience","mentor.entrance_exam_experience"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mentorships-matches.csv'
        writer = csv.writer(response)
        writer.writerow(column_names)
        for mentee in queryset:
            if mentee.mentor !=None:
                mentor=mentee.mentor
                row_contents=[
                    mentee.id,mentor.id,
                    mentee.course,mentor.occupation[0],
                    mentee.year_applied,mentor.year_applied,
                    mentee.sex,mentor.sex,
                    mentee.area_of_support,mentor.area_of_support,
                    mentee.interview_experience,mentor.interview_experience,
                    mentee.entrance_exam_experience,mentor.entrance_exam_experience
                    ]
                row = writer.writerow(row_contents)
                LogEntry.objects.log_action(
                    user_id=request.user.id, 
                    content_type_id=ct.pk,
                    object_id=mentee.pk,
                    object_repr=mentee.__str__(),
                    action_flag=CHANGE,
                    change_message="Exported Matches Info") 
        return response
    actions = [export_as_csv,"export_matches","assign_mentor","email_matches","export_matches_info"]

class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    fields = (
        'action_time', 'user', 'content_type', 'object_id',
        'object_repr', 'action_flag', 'change_message',
    )
    readonly_fields = fields
   
    list_display = (
        'action_time', 'user','action_message', 'content_type'
    )
    list_filter = (
        'action_flag', 'content_type',
    )
    search_fields = (
        'object_repr', 'change_message','user',
    )
    def action_message(self, obj):
        change_message = obj.get_change_message()
        if not change_message:
            change_message = '{}.'.format(obj.get_action_flag_display())
        return change_message
    action_message.short_description = 'action'
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']
    list_filter = ['expire_date']
    def has_change_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
        
admin.site.register(Session, SessionAdmin)
admin.site.register(MentorProfile,MentorAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)
admin.site.register(LogEntry,LogEntryAdmin)