import csv
from django.core import mail
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.sessions.models import Session
from django.utils.html import format_html
from django.http import HttpResponse
from .models import MentorProfile, MenteeProfile, MentorQualification, MenteeQualification
from .forms import MentorForm, MenteeForm
from .matching import generate_matches
from .filters import MentorListFilter, MenteeListFilter
from django.conf import settings


# TODO add default messages for email - from django.conf import settings

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
        ('Mentee Application Information', {'fields': ['course', 'mentor_need', 'mentor_help', 'mentor_relationship']})
    ]


class MentorAdmin(admin.ModelAdmin):
    inlines = [
        MentorQualificationInline, MenteeInline
    ]
    list_filter = ['occupation', 'date_joined', 'is_active', 'year_applied', MenteeListFilter]
    exclude = [""]
    form = MentorForm
    list_display = ['email', 'first_name', 'last_name', 'entrance_exam_experience', 'interview_experience',
                    'area_of_support']

    fieldsets = [
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email','work_email', 'sex']}),
        ('Background Information', {
            'fields': ['occupation', 'year_applied', 'entrance_exam_experience', 'interview_experience',
                       'area_of_support']}),
        ('Meta', {'fields': ['date_joined', 'hear_about_us', 'is_active', 'tcs_check']})
    ]
    actions = [export_as_csv]


class MenteeQualificationInline(admin.TabularInline):
    model = MenteeQualification
    extra = 0
    can_delete = True


def save_matches(request, matches, ct):
    for k, v in matches.items():
        mentor = MentorProfile.objects.get(id=v[0])
        mentee = MenteeProfile.objects.get(id=k)
        mentee.mentor = mentor
        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ct.pk,
            object_id=mentee.pk,
            object_repr=str(mentee),
            action_flag=CHANGE,
            change_message="Added mentor match")
        mentee.save()
    entry = LogEntry(user_id=request.user.id, action_flag=CHANGE, content_type_id=ct.pk,
                     change_message="Mentee-Mentor matches ran")
    entry.save()


class MenteeAdmin(admin.ModelAdmin):
    inlines = [
        MenteeQualificationInline,
    ]
    exclude = [""]
    form = MenteeForm
    list_display = ['email', 'first_name', 'last_name', 'area_of_support', 'mentor_link']
    list_filter = ['course', 'date_joined', 'accepted', 'year_applied', MentorListFilter]
    fieldsets = [
        ('Personal Information', {'fields': ['first_name', 'last_name', 'email', 'sex']}),
        ('Background Information',
         {'fields': ['year_applied', 'entrance_exam_experience', 'interview_experience', 'area_of_support']}),
        ('Application Information', {
            'fields': ['course', 'mentor_need', 'mentor_help', 'mentor_relationship', 'current_application',
                       'accepted']}),
        ('Mentor', {'fields': ['mentor']}),
        ('Meta', {'fields': ['date_joined', 'hear_about_us', 'tcs_check']})
    ]

    def mentor_link(self, obj):
        mentor = obj.mentor
        if mentor:
            admin_url = mentor.get_admin_url()
            return format_html('<a href="{}">{}</a>', admin_url, mentor)
        else:
            return None

    mentor_link.short_description = 'Mentor'

    def has_mentor(self, obj):
        mentor = obj.mentor
        if mentor:
            return True
        else:
            return False

    def generate_matches_messages(self, mentees):
        emails = []
        subject = settings.EMAIL_MATCH_SUBJECT
        slack_link_msg = f'\nPlease join our slack community to communicate with each other : {settings.SLACK_URL}'
        for mentee in mentees:
            if mentee.mentor is not None:
                mentor = mentee.mentor
                mentor_body = settings.EMAIL_MATCH_BODY + f'\nYou have been matched with mentee : {mentee.first_name}  {mentee.last_name}' + slack_link_msg + settings.DEFAULT_MSG_CLOSING
                mentee_body = settings.EMAIL_MATCH_BODY + f'\nYou have been matched with mentor : {mentor.first_name}  {mentor.last_name}' + slack_link_msg + settings.DEFAULT_MSG_CLOSING
                mentee_email = mail.EmailMessage(subject=subject, body=mentee_body, to=[mentee.email],
                                                 reply_to=[settings.DEFAULT_EMAIL_REPLY_TO])
                mentor_email = mail.EmailMessage(subject=subject, body=mentor_body, to=[mentor.email],
                                                 reply_to=[settings.DEFAULT_EMAIL_REPLY_TO])
                mentor_email.attach_file('static/mentorship/docs/Code of Conduct for Volunteers.pdf')
                mentor_email.attach_file('static/mentorship/docs/Medicine Mentor Guide 2021.docx.pdf')
                emails.append(mentor_email)
                emails.append(mentee_email)
        return emails

    @admin.action(description='Email Match(es)')
    def email_matches(self, request, queryset):
        with mail.get_connection() as connection:
            messages = self.generate_matches_messages(queryset)
            connection.send_messages(messages)

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

    actions = [export_as_csv, "assign_mentor", "export_matches_info", "email_matches"]


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
admin.site.site_header = "ACMM Database"
admin.site.site_title = "ACMM Database"
admin.site.index_title = "ACMM Database"
