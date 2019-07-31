from django import template

# Django settings from settings.py
from django.conf import settings

# Import models
from app.models import *
from django.contrib.auth.models import User

# Condition operators for models
from django.db.models import Q, When
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone, safestring

# use Library
register = template.Library()


#*********************************************************************************
#   assessment links
#*********************************************************************************  

@register.filter   
def dynamic_links(value):
    return value.lower().replace(" ","-")

#*********************************************************************************
#   Page title 
#*********************************************************************************

@register.simple_tag 
def page_title():
    return settings.PAGE_TITLE


#*********************************************************************************
#   Tag for loading css files
#*********************************************************************************

@register.simple_tag
def load_css_files(scripts = list()):

    html = []

    for script in scripts:
        html.append('<link rel="stylesheet" href="'+settings.STATIC_URL+script+'"/>')
        
    return safestring.mark_safe(''.join(html))


#*********************************************************************************
#   Tag for loading javascript files
#*********************************************************************************

@register.simple_tag
def load_javascript_files(scripts = list()):

    html = []

    for script in scripts:
        html.append('<script src="'+settings.STATIC_URL+script+'"></script>')
        
    return safestring.mark_safe(''.join(html))

#*********************************************************************************
#   PAGINATION HTML
#*********************************************************************************

@register.simple_tag
def pagination_html(page_obj, url = ""):

    dc = page_obj.paginator

    html = []
    html.append('<p class="text-center" style="background-color: #24262d; color: #ffffff; padding:7px 10px;border: 1px solid #3d404c;">')
    html.append('<strong>Page '+ str(page_obj.number)+ ' of '+ str(page_obj.paginator.num_pages)+'</strong>')
    html.append('</p>')
    html.append('<ul class="pagination pull-right" style="margin: 0px;">')

    for i in dc.page_range:
        html.append('<li>'+'<a href="'+url+'?page='+str(i)+'">'+str(i)+'</a></li>')

    html.append('</ul>')

    return safestring.mark_safe(''.join(html))

#*********************************************************************************
#   USER LIST HTML DROPDOWN 
#*********************************************************************************

@register.simple_tag
def user_list(name = '', multiple = ''):

    users = User.objects.filter(is_staff = False, is_active = True).values()

    html = ['<select class="form-control" name="'+name+'">']

    if multiple == 'multiple':
        html = ['<select name="'+name+'" class="select2_demo_3 form-control select2-hidden-accessible col-md-10" multiple="" style="width: 100%" tabindex="-1" aria-hidden="true" multiple>']
    
    for user in users:
        html.append('<option value="'+str(user["id"])+'">'+user["first_name"].title()+" "+user["last_name"].title()+" ("+user["username"]+')</option>')
    html.append('<select>')

    return safestring.mark_safe(''.join(html))

#*********************************************************************************
#   TICK MARK - ICON FOR TRUE AND FALSE
#*********************************************************************************

@register.simple_tag
def tick_mark(value):
    if value:
        html = '<span class="mdi mdi-check" style="color:#000000"></span>'
    else:
        html = '<span class="mdi mdi-close" style="color:#000000"></span>'

    return safestring.mark_safe(html)