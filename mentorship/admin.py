from django.contrib.admin.models import LogEntry, CHANGE
from django.utils.html import format_html

from .models import MentorProfile, MenteeProfile, MentorQualification, MenteeQualification
from .forms import MentorForm, MenteeForm
import csv
from django.http import HttpResponse
from django.contrib import admin
from collections import defaultdict
import pandas as pd
import numpy as np
from django.contrib.contenttypes.models import ContentType
from collections import Counter


@admin.action(description='Export Selected Profiles')
def export_as_csv(self, request, queryset):
    meta = self.model._meta
    # gets all the field names from the model
    field_names = [field.name for field in meta.fields]
    # form the cols names
    column_names = field_names + ["qualifications"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    writer = csv.writer(response)
    writer.writerow(column_names)
    # for obj in selected objects
    for obj in queryset:
        # gets all the row attributes by using fields names
        row_contents = [getattr(obj, field) for field in field_names]
        # export qualifications based on profile type
        if isinstance(obj, MenteeProfile):
            qualifications = [(q.name, q.education_level, q.grade, q.predicted) for q in
                              MenteeQualification.objects.filter(profile=obj)]
        else:
            qualifications = [(q.name, q.education_level) for q in MentorQualification.objects.filter(profile=obj)]
        row_contents.append(qualifications)
        # write row
        writer.writerow(row_contents)
    return response


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
    list_display = ['email', 'first_name', 'last_name', 'entrance_exam_experience', 'interview_experience',
                    'area_of_support']

    fieldsets = [
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email', 'sex']}),
        ('Background Information', {
            'fields': ['occupation', 'year_applied', 'entrance_exam_experience', 'interview_experience',
                       'area_of_support']}),
        ('Meta', {'fields': ['date_joined', 'hear_about_us', 'is_active']})
    ]
    actions = [export_as_csv]


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
    list_filter = ['course', 'date_joined', 'accepted', 'year_applied']
    list_display = ['email', 'first_name', 'last_name','area_of_support','mentor_link']
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

    def mentor_link(self, obj):
        mentor = obj.mentor
        if mentor:
            admin_url = mentor.get_admin_url()
            return format_html('<a href="{}">{}</a>', admin_url, mentor)
        else:
            return None
    mentor_link.short_description = 'Mentor'
    @admin.action(description='Export Matches Info')
    def export_matches_info(self, request, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        meta = self.model._meta
        column_names = ["mentee.id", "mentor.id",
                        "mentee.course", "mentor.occupation",
                        "mentee.year_applied", "mentor.year_applied",
                        "mentee.sex", "mentor.sex",
                        "mentee.area_of_support", "mentor.area_of_support",
                        "mentee.interview_experience", "mentor.interview_experience",
                        "mentee.entrance_exam_experience", "mentor.entrance_exam_experience"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mentorships-matches.csv'
        writer = csv.writer(response)
        writer.writerow(column_names)
        for mentee in queryset:
            if mentee.mentor != None:
                mentor = mentee.mentor
                row_contents = [
                    mentee.id, mentor.id,
                    mentee.course, mentor.occupation[0],
                    mentee.year_applied, mentor.year_applied,
                    mentee.sex, mentor.sex,
                    mentee.area_of_support, mentor.area_of_support,
                    mentee.interview_experience, mentor.interview_experience,
                    mentee.entrance_exam_experience, mentor.entrance_exam_experience
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

    def generate_matches(self, mentors, mentees):
        mentee_preferences = defaultdict(dict)
        for mentee in mentees:
            rankings = defaultdict(dict)
            for mentor in mentors:
                ranking = 10
                # if both the mentee and mentor applied at the same stage(grad or post-18) double ranking
                if mentor.year_applied == mentee.year_applied:
                    ranking *= 2
                # if the sex are not the same decrease ranking by 20%
                if mentor.sex != mentee.sex:
                    ranking *= 0.8
                # counts the overlapping area_of_support for both the mentee and mentor
                support_factor = len(np.intersect1d(mentor.area_of_support, mentee.area_of_support))
                # counts how much interview experience the mentor had
                interview_factor = len(mentor.interview_experience)
                # counts the overlapping exam experience
                exam_factor = len(np.intersect1d(mentor.entrance_exam_experience, mentee.entrance_exam_experience))

                # ensures the mentor can support the mentee based on their experiences
                if ('EE' in mentee.area_of_support and exam_factor == 0) or (
                        'I' in mentee.area_of_support and interview_factor == 0):
                    support_factor = 0
                # amplifies the exam factor if they need support for entrance exams
                if 'EE' in mentee.area_of_support:
                    exam_factor *= 10
                # amplifies the interview factor if they need support for interviews
                if 'I' in mentee.area_of_support:
                    interview_factor *= 10
                # calculates the mentor factor
                mentor_factor = 1 + ((exam_factor + interview_factor) * 2)
                # calculates the overall ranking
                ranking = ranking * support_factor * mentor_factor
                # if the mentor can be of use add to the ma
                if ranking > 0:
                    rankings[mentor.id] = ranking
                mentee_preferences[mentee.id] = rankings

        matches_df = pd.DataFrame(mentee_preferences).fillna(-1)
        # mentee preferneces
        mentee_pref_df = matches_df
        mentor_list = matches_df.index.tolist()
        mentor_dict = dict.fromkeys(mentor_list, 0)
        waiting_list = defaultdict(list)
        try:
            while bool(mentor_dict):
                for k, v in mentor_dict.items():
                    # chose the mentor with the highest rank
                    waiting_list[mentee_pref_df.loc[k].nlargest().index[v]].append(k)
                    mentor_dict[k] += 1
                new_mentor_dict = defaultdict(int)
                for k, v in waiting_list.items():
                    if len(v) > 1:
                        v_t = mentee_pref_df[k].filter(items=v).sort_values(ascending=True).index.tolist()
                        print(v_t)
                        for x in v_t[1:]:
                            new_mentor_dict[x] = mentor_dict[x]
                        waiting_list[k] = v_t[:1]
                mentor_dict = new_mentor_dict
        except IndexError:
            pass
        return waiting_list

    @admin.action(description='Assign a mentor to each mentee')
    def assign_mentor(self, request, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        available_mentors = MentorProfile.objects.filter(is_active=True, menteeprofile__isnull=True)
        available_medicine_mentors = available_mentors.filter(occupation__startswith='M')
        unmatched_mentees = MenteeProfile.objects.filter(mentor__isnull=True)
        unmatched_medicine_mentees = unmatched_mentees.filter(course__startswith='M')
        matches = self.generate_matches(available_medicine_mentors, unmatched_medicine_mentees)
        print(matches)

        for k, v in matches.items():
            mentor = MentorProfile.objects.get(id=v[0])
            mentee = MenteeProfile.objects.get(id=k)
            mentee.mentor = mentor
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=mentee.pk,
                object_repr=mentee.__str__(),
                action_flag=CHANGE,
                change_message="Added mentor match")
            mentee.save()
        l = LogEntry(user_id=request.user.id, action_flag=CHANGE, content_type_id=ct.pk,
                     change_message="Mentee-Mentor matches ran")
        l.save()

    actions = [export_as_csv, "assign_mentor", "export_matches_info"]


admin.site.register(MentorProfile, MentorAdmin)
admin.site.register(MenteeProfile, MenteeAdmin)
