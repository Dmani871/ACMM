from django.shortcuts import render


from .forms import MentorCreationForm


def mentor_signup_view(request):
    form = MentorCreationForm(request.POST)
    if form.is_valid():
        form.save()
    return render(request, 'mentor_signup.html', {'form': form})

