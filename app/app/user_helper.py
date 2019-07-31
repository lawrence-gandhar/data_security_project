# Django authentication
from django.contrib.auth.models import User
from app.models import UserProfile, AppPermission


def UserList():
    users = User.objects.all().select_related('profile', 'app_permissions')
    users = users.values('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active', 
            'app_permissions__record_access_size', 'app_permissions__full_access',
            'profile__profile_pic', 'profile__phone',
        ) 
    return users
    

def UserList_Table():

    users = User.objects.all().select_related('profile', 'app_permissions')
    users = users.values('id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active', 
            'app_permissions__record_access_size', 'app_permissions__full_access',
            'profile__profile_pic', 'profile__phone',
        )

    html = list()

    html.append('<table class="table table-responsive">')
    html.append('<thead>')
    html.append('<tr>')
    html.append('<td>ID</td>')
    html.append('<td>Name</td>')
    html.append('<td>Accessible Records</td>')
    html.append('<td>Has Full Access</td>')
    html.append('<td>Profile Pic</td>')
    html.append('<td>Phone</td>')
    html.append('</tr>')
    html.append('</thead><tbody>')
    for user in users:        
        html.append('<tr>')
        html.append('<td>{0}</td>'.format(user["id"]))
        html.append('<td>{0} {1}</td>'.format(user["first_name"], user["last_name"]))
        html.append('<td>{0}</td>'.format(user["app_permissions__record_access_size"]))
        html.append('<td>{0}</td>'.format(user["app_permissions__full_access"]))
        html.append('<td>{0}</td>'.format(user["profile__profile_pic"]))
        html.append('<td>{0}</td>'.format(user["profile__phone"]))
        html.append('</tr>')
    html.append('</tbody></table>')

    return ''.join(html)
