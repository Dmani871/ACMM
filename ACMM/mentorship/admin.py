from django.contrib import admin
import csv
from django.http import HttpResponse
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification
from .forms import MentorForm,MenteeForm
# Register your models here.
from django.forms import formset_factory
from django.forms import inlineformset_factory

class MentorQualificationInline(admin.TabularInline):
    model = MentorQualification
    extra=0
    can_delete=True
class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline,
    ]
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
    form = MenteeForm
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
            qualifications=[(q.name,q.education_level,q.grade,q.predicted) for q in MenteeQualification.objects.filter(profile=obj)]
            row_contents.append(qualifications)
            row = writer.writerow(row_contents)
        return response

    export_as_csv.short_description = "Export Selected Profiles"
    actions = ["export_as_csv"]


admin.site.register(MentorProfile,MentorAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)