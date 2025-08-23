from django.shortcuts import render, redirect
# feature of django that provider authentication
from django.contrib.auth import authenticate, login, logout

# django form for authentication
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    error_message = None
    form = AuthenticationForm()
    
    # when you press login button, it generates this post request
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            # get request to read username
            username = form.cleaned_data.get('username')
            # get request to read password
            password = form.cleaned_data.get('password')
            
            try:
                # function to validate the user
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('recipeApp:list')
                else:
                    error_message = 'Invalid username or password'
            except Exception as e:
                # Log the error for debugging
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Login error: {str(e)}")
                error_message = f'Login error: {str(e)}'

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'auth/login.html', context)

# function for logout functionality


def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')

def debug_view(request):
    """Simple debug view to test if the app is working"""
    import os
    from django.db import connection
    from django.contrib.auth.models import User
    
    debug_info = {
        'environment': os.environ.get('WEBSITE_HOSTNAME', 'Not in Azure'),
        'database_engine': 'postgresql' if 'AZURE_POSTGRESQL_CONNECTIONSTRING' in os.environ else 'sqlite',
        'debug_mode': os.environ.get('DJANGO_SETTINGS_MODULE', 'Unknown'),
    }
    
    # Test database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        debug_info['database_connection'] = 'OK'
    except Exception as e:
        debug_info['database_connection'] = f'ERROR: {str(e)}'
    
    # Check if users exist
    try:
        user_count = User.objects.count()
        debug_info['user_count'] = user_count
    except Exception as e:
        debug_info['user_count'] = f'ERROR: {str(e)}'
    
    context = {
        'debug_info': debug_info
    }
    return render(request, 'auth/debug.html', context)

def test_db_view(request):
    """Simple view to test database operations"""
    from django.contrib.auth.models import User
    from django.http import JsonResponse
    
    try:
        # Test basic database operations
        user_count = User.objects.count()
        
        # Get all usernames to see what users exist
        usernames = list(User.objects.values_list('username', flat=True))
        
        # Test creating a user (this will help identify if it's a write permission issue)
        test_username = f"test_user_{user_count}"
        if not User.objects.filter(username=test_username).exists():
            user = User.objects.create_user(
                username=test_username,
                email=f"{test_username}@example.com",
                password="testpass123"
            )
            created = True
        else:
            created = False
            
        return JsonResponse({
            'status': 'success',
            'user_count': user_count,
            'existing_usernames': usernames,
            'test_user_created': created,
            'test_username': test_username
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)

def test_login_view(request):
    """Test login functionality without full Django auth"""
    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import check_password
    from django.http import JsonResponse
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Try to find the user
            user = User.objects.get(username=username)
            
            # Check password
            if check_password(password, user.password):
                return JsonResponse({
                    'status': 'success',
                    'message': 'Login successful',
                    'username': user.username,
                    'is_superuser': user.is_superuser
                })
            else:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid password'
                })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': f'User "{username}" not found'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Please send POST request with username and password'
    })
