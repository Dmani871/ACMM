from django.contrib.admin.models import LogEntry, CHANGE
from django.utils.html import format_html
from django.contrib.sessions.models import Session
from .models import MentorProfile, MenteeProfile, MentorQualification, MenteeQualification
from .forms import MentorForm, MenteeForm
import csv
from django.http import HttpResponse
from django.contrib import admin
from collections import defaultdict
import pandas as pd
import numpy as np
from django.contrib.contenttypes.models import ContentType


@admin.action(description='Export Selected Profiles')
def export_as_csv(self, request, queryset):
    # gets meta data about model
    meta = self.model._meta
    # gets all the field names from the model
    field_names = [field.name for field in meta.fields]
    # form the cols names
    column_names = field_names + ["qualifications"]
    # tells browser to treat response as an attachment
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
    # returns writer object that writes to the response
    writer = csv.writer(response)
    # write cols
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


def apply_matches_weights(mentors, mentees):
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
                support_factor = 0.01
            # amplifies the exam factor if they need support for entrance exams
            if 'EE' in mentee.area_of_support:
                exam_factor *= 10
            # amplifies the interview factor if they need support for interviews
            if 'I' in mentee.area_of_support:
                interview_factor *= 10
            # calculates the mentor factor
            mentor_factor = 1 + ((exam_factor + interview_factor) * 5)
            # calculates the overall ranking
            ranking = ranking * support_factor * mentor_factor
            # if the mentor can be of use add to the ma
            if ranking > 0:
                rankings[mentor.id] = ranking
            mentee_preferences[mentee.id] = rankings
    return mentee_preferences


def stable_matching(mentee_preferences):
    matches_df = pd.DataFrame(mentee_preferences).fillna(-1)
    # mentee preferences
    mentee_pref_df = matches_df
    mentor_list = matches_df.index.tolist()
    # tracks proposals of every mentor
    mentor_dict = dict.fromkeys(mentor_list, 0)
    # list containing all proposals per a mentee
    waiting_dict = defaultdict(list)
    rejected_mentors_list = []
    # while there are still proposals to be still be made by a mentor
    #TODO:loop until all mentors in dict has no
    while bool(mentor_dict):
        for k, v in mentor_dict.items():
            try:
                # mentor highest choice propose to mentee by adding to its proposal list
                waiting_dict[mentee_pref_df.loc[k].nlargest().index[v]].append(k)
                # increment proposal counter
                mentor_dict[k] += 1
            except IndexError:
                rejected_mentors_list.append(k)
        rejected_mentors=set(rejected_mentors_list)-set(mentor_dict)
        for rejected_mentor in rejected_mentors:
            del mentor_dict[rejected_mentor]
        new_mentor_dict = defaultdict(int)
        for k, mentors in waiting_dict.items():
            # if one mentee has multiple proposals
            if len(mentors) > 1:
                # order the list of mentors by ranking
                ordered_mentors = mentee_pref_df[k].filter(items=mentors).sort_values(ascending=False).index.tolist()
                for rejected_mentor in ordered_mentors[1:]:
                    new_mentor_dict[rejected_mentor] = mentor_dict[rejected_mentor]
                # only keeps the top weighted mentor for the mentee
                waiting_dict[k] = ordered_mentors[:1]
        mentor_dict = new_mentor_dict
    return waiting_dict


def generate_matches(mentors, mentees):
    mentee_preferences = apply_matches_weights(mentors, mentees)
    return stable_matching(mentee_preferences)


def save_matches(request, matches, ct):
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


class MenteeAdmin(admin.ModelAdmin):
    inlines = [
        MenteeQualificationInline,
    ]
    exclude = [""]
    form = MenteeForm
    list_filter = ['course', 'date_joined', 'accepted', 'year_applied']
    list_display = ['email', 'first_name', 'last_name', 'area_of_support', 'mentor_link']
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
        column_names = ["mentee.id", "mentor.id",
                        "mentee.course", "mentor.occupation",
                        "mentee.year_applied", "mentor.year_applied",
                        "mentee.sex", "mentor.sex",
                        "mentee.area_of_support", "mentor.area_of_support",
                        "mentee.interview_experience", "mentor.interview_experience",
                        "mentee.entrance_exam_experience", "mentor.entrance_exam_experience"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=mentorship-matches.csv'
        writer = csv.writer(response)
        writer.writerow(column_names)
        for mentee in queryset:
            if mentee.mentor:
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
                writer.writerow(row_contents)
                LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ct.pk,
                    object_id=mentee.pk,
                    object_repr=str(mentee),
                    action_flag=CHANGE,
                    change_message="Exported Matches Info")
        return response

    @admin.action(description='Assign a mentor to each mentee')
    def assign_mentor(self, request, queryset):
        ct = ContentType.objects.get_for_model(queryset.model)
        available_mentors = MentorProfile.objects.filter(is_active=True, menteeprofile__isnull=True)
        available_medicine_mentors = available_mentors.filter(occupation__startswith='M')
        available_dentistry_mentors = available_mentors.difference(available_medicine_mentors)
        unmatched_mentees = queryset
        unmatched_medicine_mentees = unmatched_mentees.filter(course__startswith='M')
        unmatched_dentistry_mentees = unmatched_mentees.difference(unmatched_medicine_mentees)
        medicine_matches = generate_matches(available_medicine_mentors, unmatched_medicine_mentees)
        dentistry_matches = generate_matches(available_dentistry_mentors, unmatched_dentistry_mentees)
        save_matches(request, medicine_matches, ct)
        save_matches(request, dentistry_matches, ct)

    actions = [export_as_csv, "assign_mentor", "export_matches_info"]


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    fields = (
        'action_time', 'user', 'content_type', 'object_id',
        'object_repr', 'action_flag', 'change_message',
    )
    readonly_fields = fields

    list_display = (
        'action_time', 'user', 'action_message', 'content_type'
    )
    list_filter = (
        'action_flag', 'content_type',
    )
    search_fields = (
        'object_repr', 'change_message', 'user',
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
admin.site.register(MentorProfile, MentorAdmin)
admin.site.register(MenteeProfile, MenteeAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
