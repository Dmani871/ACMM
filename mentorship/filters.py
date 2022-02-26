from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class MentorListFilter(admin.SimpleListFilter):
    title = _('has mentor')

    parameter_name = 'mentor'

    def lookups(self, request, model_admin):
        return (
            ('Y', _('Yes')),
            ('N', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Y':
            return queryset.filter(mentor__isnull=False)
        if self.value() == 'N':
            return queryset.filter(mentor__isnull=True)


from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class MenteeListFilter(admin.SimpleListFilter):
    title = _('has mentees')

    parameter_name = 'mentees'

    def lookups(self, request, model_admin):
        return (
            ('Y', _('Yes')),
            ('N', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Y':
            return queryset.filter(menteeprofile__isnull=False)
        if self.value() == 'N':
            return queryset.filter(menteeprofile__isnull=True)
