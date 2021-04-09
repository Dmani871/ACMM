"""ACMM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mentorship.views import mentor_signup_view,mentee_signup_view,thank_you_view,next_year_view,applications_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mentor/signup', mentor_signup_view, name='mentor'),
    path('mentee/signup', mentee_signup_view, name='mentee'),
    path('thanks', thank_you_view, name='thanks'),
    path('next_year', next_year_view, name='next_year'),
    path('', applications_view, name='applications'),
]

admin.site.site_header = "ACMM Admin"
admin.site.site_title = "ACMM Admin Portal"
admin.site.index_title = "Welcome to ACMM Portal"