from django.contrib import admin
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

admin.site.register(MentorProfile,MentorAdmin)
admin.site.register(MenteeProfile,MenteeAdmin)