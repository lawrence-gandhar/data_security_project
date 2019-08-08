from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from app.views import *
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'app/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/registration/logout.html'), name = 'logout'),
    path('dashboard/', login_required(Dashboard.as_view()), name = 'dashboard'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('staff-management/',login_required(StaffManagement.as_view()), name = "staff_management"),
    path('edit-staff/<int:user_id>/', login_required(EditStaff.as_view()), name='edit_staff'),
    path('record-management/',login_required(RecordManagement.as_view()), name = "record_management"),
]