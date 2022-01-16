
from django.contrib import admin
from django.urls import include, path
from two_factor.urls import urlpatterns as tf_urls
import os
from ACMM.settings.env_config import env

urlpatterns = [
    path('', include(tf_urls)),
    path('mentorship/', include('mentorship.urls')),
    path('admin/',include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(env('SECRET_ADMIN_URL') + 'admin/', admin.site.urls),
]

admin.site.site_header = "ACMM Admin"
admin.site.site_title = "ACMM Admin Portal"
admin.site.index_title = "Welcome to ACMM Portal"