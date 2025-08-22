#!/bin/bash
export DJANGO_SETTINGS_MODULE=recipe_project.deployment

# Run migrations
python manage.py migrate --noinput

# Start the application
gunicorn --bind=0.0.0.0:$PORT --timeout 600 recipe_project.wsgi 