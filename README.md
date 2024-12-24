# Fitness Workout Tracker API

This is a challenge from [here](https://roadmap.sh/backend/project-ideas#9-fitness-workout-tracker).

Before running the project, you need some setups.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Then you can login as superuser or create a new user on screen.

For security checks, run `DJANGO_DEBUG=false python manage.py check --deploy`
