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
from django.contrib.auth.hashers import make_password

# Django Messaging Framework
from django.contrib import messages

# Conditional operators and exception for models
from django.db.models import Q, Count, Sum, Prefetch
from django.core.exceptions import ObjectDoesNotExist

# Paginator class import
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

# Helpers
import app.user_helper as user_helper
import app.records_helper as records_helper

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
#   STAFF/USER MANAGEMENT
#=========================================================================================

class StaffManagement(View):
    template_name = 'app/staff_management/index.html'
    js_files = ['app_files/staff_management.js']

    def get(self, request):

        page = request.GET.get('page',1)
        records_per_page = request.GET.get('per_page',None)
        
        return render(request, self.template_name, {
            "users": user_helper.UserList(page,records_per_page), 
            'staff_form': StaffForm(),
            'category_list' : records_helper.CategoryList(),
            'sub_category_list' : records_helper.SubCategoryList(),
            'brand_list' : records_helper.BrandList(),
            'pe_list' : records_helper.PEList(),
            'error_msg': None, 
            'js_files' : self.js_files,
        })


    def post(self, request):        
        staff = StaffForm(request.POST or None)

        if staff.is_valid():
            staff.full_clean()
            user = staff.save(commit=False)
            user.password = make_password(staff.cleaned_data['password'])
            user.save()
            
            app_perm = AppPermission.objects.get(user = user)
            app_perm.save()
            
            
            dec = request.POST.getlist("dedicated_to_category")
            dec_s = request.POST.getlist("dedicated_to_sub_category")
            br = request.POST.getlist("dedicated_to_brand")
            pe = request.POST.getlist("dedicated_to_pe")
            
            if len(dec) > 0:
                category = Category.objects.filter(pk__in = dec)   
                for rec in category:
                    app_perm.dedicated_to_category.add(rec)
                
                    
            if len(dec_s) > 0:
                s_category = Category.objects.filter(pk__in = dec_s)   
                for rec in s_category:
                    app_perm.dedicated_to_sub_category.add(rec)
                
                
            if len(br) > 0:
                brand = Brand.objects.filter(pk__in = br)   
                for rec in brand:
                    app_perm.dedicated_to_brand.add(rec)
                
                    
            if len(pe) > 0:
                pe = PreviousExhibition.objects.filter(pk__in = pe)   
                for rec in pe:
                    app_perm.dedicated_to_pe.add(rec)
                     
            return redirect('/staff-management/', 'refresh')
             
        return render(request, self.template_name, {
            "users": user_helper.UserList(), 
            'staff_form': StaffForm(),
            'error_msg' : 'Not a valid form! Try again',
            'js_files' : self.js_files,
        })

#=========================================================================================
#   GET SUB CATEGORY ON BASIS OF CATEGORY
#=========================================================================================

def get_sub_category(request):
    sub_cat_list = request.GET.getlist("cat_id[]")
    
    if len(sub_cat_list) > 0:
        sub_cats = records_helper.SubCategoryList(sub_cat_list)
        
        html = []
        for sub in sub_cats:
            html.append('<option value="'+str(sub.id)+'">'+str(sub)+'</option>');
        return HttpResponse(''.join(html))
    return HttpResponse('')   

#=========================================================================================
#   STAFF/USER EDIT
#=========================================================================================

class EditStaff(View):
    template_name = 'app/staff_management/edit_staff.html'
    js_files = ['app_files/staff_management.js']
    

    def get(self, request, *args, **kwargs):
        staff = user_helper.UserDetailsObject(kwargs["user_id"]) 

        if staff is None:
            return HttpResponseForbidden()

        staff_form  = UpdateStaffForm(instance = staff, prefix='staff')

        try:
            app_permission = AppPermissionForm(instance = staff.app_permissions, prefix='perms')
        except:
            perms = AppPermission.objects.create(user=staff)
            perms = perms.refresh_from_db()
            app_permission = AppPermissionForm(instance = perms, prefix='perms')

        try:
            user_profile = ProfileForm(instance = staff.profile, prefix='profile')
        except:
            profile = UserProfile.objects.create(user=staff)
            profile = profile.refresh_from_db()
            user_profile = ProfileForm(instance = profile, prefix='profile')
            
        return render(request, self.template_name, {
            'staff_form': staff_form, 
            'user_profile': user_profile,
            'app_permission':app_permission,
            'error_msg': None, 
            'staff':staff,
            'category_list' : records_helper.CategoryList(),
            'sub_category_list' : records_helper.SubCategoryList(),
            'brand_list' : records_helper.BrandList(),
            'pe_list' : records_helper.PEList(),
            'js_files' : self.js_files,
        })


    def post(self, request, *args, **kwargs):

        user = user_helper.UserDetailsObject(kwargs["user_id"]) 
        
        if user is None:
            return HttpResponseForbidden()

        staff_form = UpdateStaffForm(request.POST or None, instance = user, prefix='staff')
        user_profile = ProfileForm(request.POST or None,  request.FILES or None, instance = user.profile, prefix='profile')
        app_permission = AppPermissionForm(request.POST or None, instance = user.app_permissions, prefix='perms')

        if staff_form.is_valid() and user_profile.is_valid() and app_permission.is_valid():
            staff_form.full_clean()
            staff = staff_form.save(commit = False)
            staff.profile = user_profile.save()
            staff.app_permissions = app_permission.save()
            staff.save()
            
            app_perm = AppPermission.objects.get(user = user)
            app_perm.save()
            
            app_perm.dedicated_to_category.clear()
            app_perm.dedicated_to_sub_category.clear()
            app_perm.dedicated_to_brand.clear()  
            app_perm.dedicated_to_pe.clear()      
            
            
            dec = request.POST.getlist("dedicated_to_category")
            dec_s = request.POST.getlist("dedicated_to_sub_category")
            br = request.POST.getlist("dedicated_to_brand")
            pe = request.POST.getlist("dedicated_to_pe")
            
            if len(dec) > 0:
                category = Category.objects.filter(pk__in = dec)                   
                for rec in category:
                    app_perm.dedicated_to_category.add(rec)
                
                    
            if len(dec_s) > 0:
                s_category = Category.objects.filter(pk__in = dec_s)                  
                for rec in s_category:
                    app_perm.dedicated_to_sub_category.add(rec)
                
                
            if len(br) > 0:
                brand = Brand.objects.filter(pk__in = br)                                
                for rec in brand:
                    app_perm.dedicated_to_brand.add(rec)
                
                    
            if len(pe) > 0:
                pe = PreviousExhibition.objects.filter(pk__in = pe)  
                app_perm.dedicated_to_pe.clear()  
                for rec in pe:
                    app_perm.dedicated_to_pe.add(rec)
             
                        
            return redirect('/staff-management/', parmanent = True)
        else:
            return render(request, self.template_name, {
                'staff_form': staff_form, 
                'user_profile': user_profile,
                'app_permission':app_permission,
                'error_msg': None, 
                'staff':user,
                'category_list' : records_helper.CategoryList(),
                'sub_category_list' : records_helper.SubCategoryList(),
                'brand_list' : records_helper.BrandList(),
                'pe_list' : records_helper.PEList(),
                'js_files' : self.js_files,
            })

 