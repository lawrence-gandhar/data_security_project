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

    def get(self, request):

        page = request.GET.get('page',1)
        records_per_page = request.GET.get('per_page',None)

        return render(request, self.template_name, {
            "users": user_helper.UserList(page,records_per_page), 
            'staff_form': StaffForm(),
            'error_msg': None, 
        })


    def post(self, request):        
        staff = StaffForm(request.POST or None)

        if staff.is_valid():
            try:
                staff.full_clean()
                staff.save()
                return redirect('/staff-management/', 'refresh')
            except:
                error_msg = 'Error Occurred! Try again with valid data'
            
                return render(request, self.template_name, {
                    "users": user_helper.UserList(), 
                    'staff_form': StaffForm(),
                    'error_msg' : error_msg,
                })
        return render(request, self.template_name, {
            "users": user_helper.UserList(), 
            'staff_form': StaffForm(),
            'error_msg' : 'Not a valid form! Try again',
        })


#=========================================================================================
#   STAFF/USER EDIT
#=========================================================================================

class EditStaff(View):
    template_name = 'app/staff_management/edit_staff.html'

    def get(self, request, *args, **kwargs):
        user = user_helper.UserDetailsObject(kwargs["user_id"]) 

        if user is None:
            return HttpResponseForbidden()

        staff_form  = UpdateStaffForm(instance = user, prefix='staff')

        try:
            app_permission = AppPermissionForm(instance = user.app_permissions, prefix='perms')
        except:
            perms = AppPermission.objects.create(user=user)
            perms = perms.refresh_from_db()
            app_permission = AppPermissionForm(instance = perms, prefix='perms')

        try:
            user_profile = ProfileForm(instance = user.profile, prefix='profile')
        except:
            profile = UserProfile.objects.create(user=user)
            profile = profile.refresh_from_db()
            user_profile = ProfileForm(instance = profile, prefix='profile')

        return render(request, self.template_name, {
            'staff_form': staff_form, 
            'user_profile': user_profile,
            'app_permission':app_permission,
            'error_msg': None, 
            'staff':user,
        })


    def post(self, request, *args, **kwargs):

        user = user_helper.UserDetailsObject(kwargs["user_id"]) 

        if user is None:
            return HttpResponseForbidden()

        staff_form = UpdateStaffForm(request.POST or None, instance = user, prefix='staff')
        user_profile = ProfileForm(request.POST or None, instance = user.profile, prefix='profile')
        app_permission = AppPermissionForm(request.POST or None, instance = user.app_permissions, prefix='perms')

        if staff_form.is_valid() and user_profile.is_valid():
            staff_form.full_clean()
            staff = staff_form.save(commit = False)
            staff.profile = user_profile.save()
            staff.app_permissions = app_permission.save()
            staff.save()
            return redirect('/staff-management/', parmanent = True)
        else:
            return render(request, self.template_name, {
                'staff_form': staff_form, 
                'user_profile': user_profile,
                'app_permission':app_permission,
                'error_msg': None, 
                'staff':user,
            })

        
        