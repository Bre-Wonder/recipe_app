#!/bin/bash
export DJANGO_SETTINGS_MODULE=recipe_project.deployment

# Run migrations
python manage.py migrate --noinput

# Create test user if it doesn't exist
python manage.py create_test_user

# Start the application
gunicorn --bind=0.0.0.0:$PORT --timeout 600 recipe_project.wsgi 