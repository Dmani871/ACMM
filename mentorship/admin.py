from django.contrib import admin
from .models import MentorProfile, MenteeProfile, MentorQualification, MenteeQualification
from .forms import MentorForm, MenteeForm


class MentorQualificationInline(admin.TabularInline):
    model = MentorQualification
    extra = 0
    can_delete = True


class MenteeInline(admin.StackedInline):
    model = MenteeProfile
    extra = 0
    can_delete = False
    show_change_link = True
    form = MenteeForm
    fieldsets = [
        ('Mentee Personal Information', {'fields': ['first_name', 'last_name', 'email', 'sex']}),
        ('Mentee Background Information',
         {'fields': ['year_applied', 'entrance_exam_experience', 'interview_experience', 'area_of_support']}),
        ('Mentee Application Information', {'fields': ['course', 'mentor_need', 'mentor_help', 'mentor_relationship']}),
    ]


class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline, MenteeInline
    ]
    list_filter = ['occupation', 'date_joined', 'is_active', 'year_applied']
    exclude = [""]
    form = MentorForm
    list_display = ['email', 'first_name', 'last_name']

    fieldsets = [
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email', 'sex']}),
        ('Background Information', {
            'fields': ['occupation', 'year_applied', 'entrance_exam_experience', 'interview_experience',
                       'area_of_support']}),
        ('Meta', {'fields': ['date_joined', 'hear_about_us', 'is_active']})
    ]


class MenteeQualificationInline(admin.TabularInline):
    model = MenteeQualification
    extra = 0
    can_delete = True


class MenteeAdmin(admin.ModelAdmin):
    inlines = [
        MenteeQualificationInline,
    ]
    exclude = [""]
    form = MenteeForm
    list_filter = ['course', 'date_joined', 'accepted', 'year_applied', 'hear_about_us']
    list_display = ['email', 'first_name', 'last_name', 'entrance_exam_experience', 'interview_experience',
                    'area_of_support']
    fieldsets = [
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email', 'sex']}),
        ('Background Information',
         {'fields': ['year_applied', 'entrance_exam_experience', 'interview_experience', 'area_of_support']}),
        ('Application Information', {
            'fields': ['course', 'mentor_need', 'mentor_help', 'mentor_relationship', 'current_application',
                       'accepted']}),
        ('Mentor', {'fields': ['mentor']}),
        ('Meta', {'fields': ['date_joined', 'hear_about_us']})
    ]


admin.site.register(MentorProfile, MentorAdmin)
admin.site.register(MenteeProfile, MenteeAdmin)
