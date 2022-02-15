from django.shortcuts import render

def thank_you_view(request):
    return render(request,  'mentorship/thank_you.html',{'page_title':'Thank You'})