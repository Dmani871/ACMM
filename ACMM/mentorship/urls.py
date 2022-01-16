from django.urls import path

from . import views


app_name = 'mentorship'
urlpatterns = [
    path('', views.applications_view, name='index'),
    path('mentor/signup',views.mentor_signup_view, name='mentor'),
    path('mentee/signup',views.mentee_signup_view, name='mentee'),
    path('thanks',views.thank_you_view, name='thank_you'),
    path('next_year',views.next_year_view, name='next_year'),
    
]