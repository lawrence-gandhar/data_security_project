from django.urls import path, include, re_path
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from app.main_views import *
from app.views import * 

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name = 'app/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'app/registration/logout.html'), name = 'logout'),
    path('dashboard/', never_cache(login_required(Dashboard.as_view())), name = 'dashboard'),
    re_path(r'^accounts/*', RedirectView.as_view(pattern_name='login', permanent=True)),
    path('staff-management/', never_cache(login_required(StaffManagement.as_view())), name = "staff_management"),
    path('edit-staff/<int:user_id>/', never_cache(login_required(EditStaff.as_view())), name='edit_staff'),
    path('record-management/', never_cache(login_required(RecordManagement.as_view())), name = "record_management"),
    path('activate_records/', login_required(activate_records), name='activate_records'),
    path('auto_assign/', login_required(auto_assign), name='auto_assign'),
    path('staff-record/', never_cache(login_required(StaffRecord.as_view())), name='staff_record'),
    path('staff-record/<int:record_id>/', never_cache(login_required(StaffRecord.as_view())), name='staff_record'),
    path('get_sub_category/', login_required(get_sub_category), name='get_sub_category'),
    path('set_completed/', login_required(set_completed), name='set_completed'),
    path('delete_file_data/', login_required(delete_file_data), name='delete_file_data'),
    path('get_record_details/', login_required(get_record_details), name='get_record_details'),   
    path('assign_selected_records/', login_required(assign_selected_records), name='assign_selected_records'),
    path('approve_records/', login_required(approve_records), name='approve_records'),
]