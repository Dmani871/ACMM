from django.contrib import admin
from .models import MentorProfile
from .forms import MentorCreationForm
# Register your models here.


class MentorAdmin(admin.ModelAdmin):
    form = MentorCreationForm
    list_display = ('first_name','last_name','email')


admin.site.register(MentorProfile,MentorAdmin)