from django.forms import *
from app.models import *

class StaffForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser',)
        widgets = {
            'username': TextInput(attrs={'class':'form-control input-sm'}),
            'password': PasswordInput(attrs={'class':'form-control input-sm'}),
            'first_name': TextInput(attrs={'class':'form-control input-sm'}),
            'last_name': TextInput(attrs={'class':'form-control input-sm'}),
            'email': EmailInput(attrs={'class':'form-control input-sm'}), 
            'is_active': CheckboxInput(attrs={'value':'1', 'checked':'true'}),
            'is_staff': CheckboxInput(attrs={'value':'1',}),
            'is_superuser': CheckboxInput(attrs={'value':'1',}),
        }
        
class UpdateStaffForm(ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser',)
        widgets = {
            'first_name': TextInput(attrs={'class':'form-control input-sm'}),
            'last_name': TextInput(attrs={'class':'form-control input-sm'}),
            'email': EmailInput(attrs={'class':'form-control input-sm'}), 
            'is_active': CheckboxInput(attrs={'value':'1', 'checked':'true'}),
            'is_staff': CheckboxInput(attrs={'value':'1',}),
            'is_superuser': CheckboxInput(attrs={'value':'1',}),
        }



class ProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'phone')
        widgets = {
            'profile_pic': FileInput(attrs={'class':'form-control input-sm', 'required':False, 'style':'line-height: 14px; font-size: 10px; padding: 4px 5px;'}),
            'phone': TextInput(attrs={'class':'form-control input-sm'}),
        }


class AppPermissionForm(ModelForm):
    
    class Meta:
        model = AppPermission
        fields = ('record_access_size', 'full_access', 'read_only_mode')
                
        widgets = {
            'read_only_mode': CheckboxInput(attrs={'value':'1',}),
            'record_access_size': TextInput(attrs={'class':'form-control input-sm'}),
            'full_access': CheckboxInput(attrs={'value':'1',}),
        }
        
        
        
        
        
        