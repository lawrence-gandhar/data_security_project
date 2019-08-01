# Django authentication
from django.contrib.auth.models import User
from app.models import UserProfile, AppPermission


def UserList():
    users = User.objects.all().select_related('profile', 'app_permissions')
    users = users.values('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active', 
            'app_permissions__record_access_size', 'app_permissions__full_access', 'app_permissions__read_only_mode',
            'profile__profile_pic', 'profile__phone',
        ) 
    return users

  
def UserDetailsObject(user_id):
    user = User.objects.select_related('profile', 'app_permissions').get(pk = int(user_id))
    return user  