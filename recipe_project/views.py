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

def serve_media(request, path):
    """Serve media files in production"""
    from django.conf import settings
    from django.http import FileResponse, Http404
    import os
    
    # Security check - only serve files from media directory
    if '..' in path or path.startswith('/'):
        raise Http404("File not found")
    
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if not os.path.exists(file_path):
        raise Http404("File not found")
    
    # Get file extension to set content type
    import mimetypes
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response

def check_recipe_images(request):
    """Check recipe images status"""
    from recipeApp.models import Recipe
    from django.http import JsonResponse
    import os
    
    try:
        recipes = Recipe.objects.all()
        recipe_data = []
        
        for recipe in recipes:
            # Check if image file exists
            image_exists = False
            image_path = None
            if recipe.pic:
                image_path = os.path.join('media', str(recipe.pic))
                image_exists = os.path.exists(image_path)
            
            recipe_data.append({
                'id': recipe.id,
                'name': recipe.name,
                'pic_field': str(recipe.pic) if recipe.pic else 'None',
                'pic_url': recipe.pic.url if recipe.pic else 'None',
                'image_exists': image_exists,
                'image_path': image_path
            })
        
        return JsonResponse({
            'status': 'success',
            'recipe_count': len(recipe_data),
            'recipes': recipe_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Check failed: {str(e)}'
        }, status=500)
