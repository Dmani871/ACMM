from django.shortcuts import render

def thank_you_view(request):
    return render(request,  'mentorship/thank_you.html',{'page_title':'Thank You'})

def next_year_view(request):
    return render(request,  'mentorship/next_year.html',{'page_title':'Apply Next Year'})