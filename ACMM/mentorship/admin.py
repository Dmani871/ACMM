from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification
from .forms import MentorForm,MenteeForm
# Register your models here.
from django.forms import formset_factory
from django.forms import inlineformset_factory
from collections import defaultdict

class MentorQualificationInline(admin.TabularInline):
    model = MentorQualification
    extra=0
    can_delete=True
class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline,
    ]
    search_fields = ['first_name','last_name','email']
    list_filter = ['occupation','date_joined','is_active']
    exclude = [""]
    form = MentorForm
    list_display = ('first_name','last_name','email')
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
            qualifications=[(q.name,q.education_level) for q in MentorQualification.objects.filter(profile=obj)]
            row_contents.append(qualifications)
            row = writer.writerow(row_contents)
        return response

    export_as_csv.short_description = "Export Selected Profiles"
    actions = ["export_as_csv"]

    

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
    list_filter = ['course','date_joined']
    
    list_display = ('first_name','last_name','email','assigned_mentor')
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
        available_mentors = MentorProfile.objects.filter(is_active=True)
        available_mentors=list(available_mentors)
        
        for mentee in queryset:
            match=[None,0]
            for mentor in available_mentors:
                ranking=0
                if mentee.course in ["Medicine","Graduate Medicine"] and not "Dent" in mentor.occupation:
                    ranking=100000
                elif mentee.course=="Dentistry" and "Dent" in mentor.occupation:
                    ranking=100000
                if mentor.year_applied==mentee.year_applied:
                    ranking=ranking*100
                if mentor.application_strength in mentee.area_of_support:
                    ranking=ranking*2
                if mentor.sex!=mentee.sex:
                    ranking=ranking*0.7
                entrance_exam_experience_factor = len(set.intersection(set(mentor.entrance_exam_experience), set(mentee.entrance_exam_experience)))+1
                interview_experience_factor = len(set.intersection(set(mentor.interview_experience), set(mentee.interview_experience)))+1
                support_factor = len(set.intersection(set(mentor.area_of_support), set(mentee.area_of_support)))+1
                mentee_qualifications=[q.name for q in MenteeQualification.objects.filter(profile=mentee)]
                mentor_qualifications=[q.name for q in MentorQualification.objects.filter(profile=mentor)]
                subject_factor = len(set.intersection(set(mentor_qualifications), set(mentee_qualifications)))+1
                ranking=ranking*entrance_exam_experience_factor*interview_experience_factor*support_factor*subject_factor
                
                
                if ranking > match[1]:
                    match[0]=mentor
                    match[1]=ranking

            if match[0] != None:
                available_mentors.remove(match[0])
                mentee.assigned_mentor=match[0]
                mentee.save()
        #for x in queryset:print(x);
    assign_mentor.short_description = "Assign a mentor to each mentee"
    actions = ["export_as_csv","assign_mentor"]


admin.site.register(MentorProfile,MentorAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)