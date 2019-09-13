# Django authentication
from django.contrib.auth.models import User
from app.models import UserProfile, AppPermission
from django.core.paginator import Paginator

def UserList(page = None, records_per_page = None):
    users = User.objects.all().select_related('profile', 'app_permissions').order_by('id')
    
    per_page = 25
    if records_per_page is not None:
        per_page = records_per_page

    if page is None:
        page = 1
    
    paginator = Paginator(users, per_page)
    users = paginator.get_page(page)
    return users

  
def UserDetailsObject(user_id):
    user = User.objects.select_related('profile', 'app_permissions').get(pk = int(user_id))
    return user  
    
def StaffList():
    users = User.objects.filter(is_active = True, is_staff = True, is_superuser = False)
    users = users.values('id', 'username', 'first_name', 'last_name').order_by('id')
    
    return users