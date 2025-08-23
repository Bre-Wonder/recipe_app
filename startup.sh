#!/bin/bash
export DJANGO_SETTINGS_MODULE=recipe_project.deployment

echo "Starting deployment process..."

# Check and setup database
echo "Checking database status..."
python manage.py check_db

# Check if database setup was successful
if [ $? -eq 0 ]; then
    echo "Database setup completed successfully"
    
    # Create test user if it doesn't exist
    echo "Creating test user..."
    python manage.py create_test_user
    
    # Start the application
    echo "Starting application..."
    gunicorn --bind=0.0.0.0:$PORT --timeout 600 recipe_project.wsgi
else
    echo "Database setup failed!"
    exit 1
fi 