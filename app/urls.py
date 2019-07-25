from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from app.views import *

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'app/registration/login.html'), name='login'),
]