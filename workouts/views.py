from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'workouts/home.html')

@login_required
def some_protected_view(request):
    # Your protected view logic here
    pass 