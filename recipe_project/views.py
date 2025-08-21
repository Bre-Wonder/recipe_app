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
