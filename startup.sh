#!/bin/bash
export DJANGO_SETTINGS_MODULE=recipe_project.deployment
gunicorn --bind=0.0.0.0:$PORT --timeout 600 recipe_project.wsgi 