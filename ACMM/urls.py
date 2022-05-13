from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    path('mentorship/', include('mentorship.urls', namespace='mentorship')),
    path(settings.ADMIN_URL + 'admin', admin.site.urls),
    path('', include(tf_urls))
]
