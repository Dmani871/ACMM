from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from two_factor.urls import urlpatterns as tf_urls
from django.conf.urls.static import static

urlpatterns = [
    path('mentorship/', include('mentorship.urls', namespace='mentorship')),
    path(settings.ADMIN_URL + 'admin', admin.site.urls),
    path('', include(tf_urls))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
