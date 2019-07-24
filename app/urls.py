from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
import app.views

urlpatterns = [
    path('', app.views.index, name=''),
]