# Django authentication
from django.contrib.auth.models import User
from app.models import UserProfile, AppPermission
from django.core.paginator import Paginator

from django.db.models import Q, Count, Sum, Prefetch


def UserList(page = None, records_per_page = None, search = None):
    users = User.objects

    if search is not None:
        users = users.filter(Q(username__icontains = search) | 
            Q(first_name__icontains = search) | 
            Q(last_name__icontains = search) |
            Q(email__icontains = search))
    else:
        users = users.all()

    users = users.select_related('profile', 'app_permissions').order_by('id')

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