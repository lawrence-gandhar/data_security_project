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
        