from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workout
from .forms import WorkoutForm

def home(request):
    if request.user.is_authenticated:
        workouts = Workout.objects.filter(user=request.user).order_by('-date')[:5]
        return render(request, 'workouts/home.html', {'workouts': workouts})
    return render(request, 'workouts/home.html')

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user)
    return render(request, 'workouts/workout_list.html', {'workouts': workouts})

@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Workout created successfully!')
            return redirect('workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'workouts/workout_form.html', {'form': form, 'title': 'Create Workout'}) 

@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Workout deleted successfully!')
        return redirect('workout_list')
    return render(request, 'workouts/workout_confirm_delete.html', {'workout': workout}) 