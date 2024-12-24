from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workout, Exercise, WorkoutExercise
from .forms import WorkoutForm, ExerciseForm, WorkoutExerciseForm

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

@login_required
def workout_edit(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    workout_exercises = workout.workoutexercise_set.all()

    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        exercise_form = WorkoutExerciseForm(request.user, request.POST)
        
        if 'add_exercise' in request.POST and exercise_form.is_valid():
            workout_exercise = exercise_form.save(commit=False)
            workout_exercise.workout = workout
            workout_exercise.order = workout_exercises.count()
            workout_exercise.save()
            messages.success(request, 'Exercise added to workout!')
            return redirect('workout_edit', pk=pk)
            
        elif 'update_workout' in request.POST and form.is_valid():
            form.save()
            messages.success(request, 'Workout updated successfully!')
            return redirect('workout_list')
    else:
        form = WorkoutForm(instance=workout)
        exercise_form = WorkoutExerciseForm(request.user)
    
    return render(request, 'workouts/workout_form.html', {
        'form': form,
        'exercise_form': exercise_form,
        'workout': workout,
        'workout_exercises': workout_exercises,
        'title': 'Edit Workout'
    })

@login_required
def exercise_list(request):
    exercises = Exercise.objects.filter(user=request.user)
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            messages.success(request, 'Exercise created successfully!')
            return redirect('exercise_list')
    else:
        form = ExerciseForm()
    return render(request, 'workouts/exercise_list.html', {
        'exercises': exercises,
        'form': form
    })

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    workout_exercises = workout.workoutexercise_set.all()
    return render(request, 'workouts/workout_detail.html', {
        'workout': workout,
        'workout_exercises': workout_exercises,
    })

@login_required
def workout_exercise_delete(request, workout_pk, exercise_pk):
    workout_exercise = get_object_or_404(
        WorkoutExercise,
        workout__pk=workout_pk,
        pk=exercise_pk,
        workout__user=request.user
    )
    workout_exercise.delete()
    messages.success(request, 'Exercise removed from workout!')
    return redirect('workout_detail', pk=workout_pk) 