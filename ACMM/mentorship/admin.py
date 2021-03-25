from django.contrib import admin
from .models import MentorProfile,Qualification
from .forms import MentorForm,QualificationForm
# Register your models here.
from django.forms import formset_factory
from django.forms import inlineformset_factory
class QualificationInline(admin.TabularInline):
    model = Qualification
    extra=0
    can_delete=True
class MentorAdmin(admin.ModelAdmin):
    inlines = [
        QualificationInline,
    ]
    form = MentorForm
    list_display = ('first_name','last_name','email')


admin.site.register(MentorProfile,MentorAdmin)