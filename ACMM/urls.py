from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('mentorship/', include('mentorship.urls')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(settings.ADMIN_URL, admin.site.urls)
]
