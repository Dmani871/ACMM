from django.urls import path
from . import views

app_name = 'mentorship'
urlpatterns = [
    path('thanks' ,views.thank_you_view, name='thank_you'),
]