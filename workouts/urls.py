from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/create/', views.workout_create, name='workout_create'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/edit/', views.workout_edit, name='workout_edit'),
    path('workouts/<int:pk>/delete/', views.workout_delete, name='workout_delete'),
    path('exercises/', views.exercise_list, name='exercise_list'),
    path('workouts/<int:workout_pk>/exercises/<int:exercise_pk>/delete/',
         views.workout_exercise_delete, name='workout_exercise_delete'),
] 