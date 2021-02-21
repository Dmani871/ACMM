from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,MentorProfile,MenteeProfile
from .forms import UserCreationForm
# Define an inline admin descriptor for MentorProfile model


class MentorProfileInline(admin.StackedInline):
    model = MentorProfile
    can_delete = True
    verbose_name_plural = 'Mentor Profile'
    fk_name = 'user'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    #form = UserChangeForm
    #add_form = UserCreationForm
    inlines = (MentorProfileInline,)
    list_display = ('email', 'first_name','last_name','get_is_mentor')
    list_select_related = ('profile', )
    list_filter = ('is_admin','is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name','last_name','password',)}),
        ('Personal info', {'fields': ('is_staff',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','password1', 'password2'),
        }),
    )
    def get_is_mentor(self, instance):
        return instance.profile.is_mentor
    get_is_mentor.short_description = 'Mentor'

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class MenteeAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name']
    actions = ['make_published']
    def make_published(self, request, queryset):
        print('je')
        print()
        for x in queryset:
            print(x);
    make_published.short_description = "Mark selected stories as published"


# Re-register UserAdmin
admin.site.register(User, UserAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)
admin.site.register(MentorProfile)
admin.site.unregister(Group)