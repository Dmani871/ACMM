from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification
from .forms import MentorForm,MenteeForm
# Register your models here.
from django.forms import formset_factory
from django.forms import inlineformset_factory
from collections import defaultdict
import numpy as np
import pandas as pd

class MentorQualificationInline(admin.TabularInline):
    model = MentorQualification
    extra=0
    can_delete=True
class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline,
    ]
    search_fields = ['first_name','last_name','email']
    list_filter = ['occupation','date_joined','is_active','sex','year_applied']
    exclude = [""]
    form = MentorForm
    list_display = ['first_name','last_name','email']

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
    
    
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        column_names= field_names+["Qualifications"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(column_names)

        for obj in queryset:
            row_contents=[getattr(obj, field) for field in field_names]
            qualifications=[(q.name,q.education_level,q.grade,q.predicted) for q in MenteeQualification.objects.filter(profile=obj)]
            row_contents.append(qualifications)
            row = writer.writerow(row_contents)
        return response

    export_as_csv.short_description = "Export Selected Profiles"
    
    
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
    actions = ["export_as_csv","assign_mentor"]


admin.site.register(MentorProfile,MentorAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)