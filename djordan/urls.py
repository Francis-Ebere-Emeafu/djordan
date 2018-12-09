"""djordan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from djordan import views


urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('room/', include('room.urls')),
    path('profile/', include('user_profile.urls')),
    # path('accounts/login/', TemplateView.as_view(template_name="registration/login.html"), name='login'),
    # path('accounts/logout/', auth_views.logout_then_login, name='logout'),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='user_profile/login.html')),
    path('accounts/', include('django.contrib.auth.urls')), # django built-in auth library REGISTRATION FOLDER
    # path('events2/', include('events2.urls')),
]
