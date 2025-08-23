"""
URL configuration for recipe_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, logout_view, debug_view, test_db_view, test_login_view, setup_database_view, test_media_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipeApp.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('debug/', debug_view, name='debug'),
    path('test-db/', test_db_view, name='test_db'),
    path('test-login/', test_login_view, name='test_login'),
    path('setup-db/', setup_database_view, name='setup_db'),
    path('test-media/', test_media_view, name='test_media'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
