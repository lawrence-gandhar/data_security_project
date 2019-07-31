# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# IntegrityError Exception for checking duplicate entry, 
# connection import to establish connection to database 
from django.db import IntegrityError, connection 

# Used for serializing object data to json string
from django.core.serializers.json import DjangoJSONEncoder 
from django.core.serializers import serialize

# Django HTTP Request
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseRedirect, JsonResponse

# Generic views as Class
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views import View

# system imports
import sys, os, csv, json, datetime, calendar, re

# Django utils
from django.utils import timezone, safestring
from django.utils.decorators import method_decorator

# Django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Django Messaging Framework
from django.contrib import messages

# Conditional operators and exception for models
from django.db.models import Q, Count, Sum, Prefetch
from django.core.exceptions import ObjectDoesNotExist

# Paginator class import
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Helpers
import app.user_helper as user_helper

# Forms
from app.forms import *

#
#***************************************************************************************
# Forgot Password
#***************************************************************************************
def forgot_password(request):
    template_name = 'registration/forgot_password.html'
    return render(request, template_name, {})

#=========================================================================================
#   DASHBOARD
#=========================================================================================

class Dashboard(View):
    
    template_name = 'app/dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {})


#=========================================================================================
#   STAFF/USER MANAGEMENT
#=========================================================================================

class StaffManagement(View):
    template_name = 'app/staff_management/index.html'

    users = user_helper.UserList()      

    def get(self, request):
        return render(request, self.template_name, {
            "users": self.users, 
            'staff_form': StaffForm(),
            'error_msg': None, 
        })


    def post(self, request):        
        staff = StaffForm(request.POST or None)

        if staff.is_valid:
            try:
                staff.save()
                return redirect('/staff-management/', 'refresh')
            except:
                error_msg = 'Error Occurred! Try again with valid data'
            
                return render(request, self.template_name, {
                    "users": self.users, 
                    'staff_form': StaffForm(),
                    'error_msg' : error_msg,
                })
        return render(request, self.template_name, {
            "users": self.users, 
            'staff_form': StaffForm(),
            'error_msg' : 'Not a valid form! Try again',
        })


#=========================================================================================
#   STAFF/USER EDIT
#=========================================================================================

class EditStaff(View):
    template_name = 'app/staff_management/edit_staff.html'

    def get(self, request, *args, **kwargs):
        user = user_helper.UserDetails(kwargs["user_id"]) 

        if user is None:
            return HttpResponseForbidden()

        return render(request, self.template_name, {
            'staff_form': EditStaffForm().staff, 
            'user_profile': EditStaffForm().user_profile,
            'app_permission':EditStaffForm.app_permission,
            'error_msg': None, 
            'staff':user,
        })