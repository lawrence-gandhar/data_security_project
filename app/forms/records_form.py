from django.forms import *
from app.models import *

class FileSubmissionForm(ModelForm):
    
    class Meta:
        model = FileSubmission
        fields = ('record_file_name', 'is_active')
        widgets = {
            'record_file_name': FileInput(attrs={'class':'form-control input-sm', 'required':False, 'style':'line-height: 14px; font-size: 10px; padding: 4px 5px;'}),
            'is_active': CheckboxInput(attrs={'value':'1', 'checked':'true'}),
        }