from django.shortcuts import render, redirect
# feature of django that provider authentication
from django.contrib.auth import authenticate, login, logout

# django form for authentication
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    error_message = None
    form = AuthenticationForm()
    # when yu press login button, it generates this post request
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            # get request to read username
            username = form.cleaned_data.get('username')
            # get request to read password
            password = form.cleaned_data.get('password')
            # function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipeApp:list')
            else:
                error_message = 'oooops... something went wrong'

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
    context = {
        'debug_info': {
            'environment': os.environ.get('WEBSITE_HOSTNAME', 'Not in Azure'),
            'database_engine': 'postgresql' if 'AZURE_POSTGRESQL_CONNECTIONSTRING' in os.environ else 'sqlite',
            'debug_mode': os.environ.get('DJANGO_SETTINGS_MODULE', 'Unknown'),
        }
    }
    return render(request, 'auth/debug.html', context)
