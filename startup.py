#!/usr/bin/env python
"""
Startup script for Azure App Service
"""
import os
import sys
import subprocess
import time

def run_command(command, description):
    """Run a command and return success status"""
    print(f"Running: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def main():
    """Main startup function"""
    print("=== Azure App Service Startup ===")
    
    # Set environment variables
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.deployment')
    
    # Check if we're in Azure
    if 'WEBSITE_HOSTNAME' not in os.environ:
        print("Not in Azure environment, skipping database setup")
        return
    
    print(f"Running in Azure: {os.environ.get('WEBSITE_HOSTNAME')}")
    
    # Step 1: Run migrations
    print("\n=== Step 1: Running migrations ===")
    if not run_command("python manage.py migrate --noinput", "Database migrations"):
        print("Migrations failed!")
        return
    
    # Step 2: Create test user
    print("\n=== Step 2: Creating test user ===")
    run_command("python manage.py create_test_user", "Create test user")
    
    # Step 3: Start the application
    print("\n=== Step 3: Starting application ===")
    port = os.environ.get('PORT', '8000')
    start_command = f"gunicorn --bind=0.0.0.0:{port} --timeout 600 recipe_project.wsgi"
    
    print(f"Starting with command: {start_command}")
    os.system(start_command)

if __name__ == "__main__":
    main() 