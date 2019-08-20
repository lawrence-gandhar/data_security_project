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
            
            if request.POST["dedicated_to_category"] != "":
                category = Category.objects.get(pk = request.POST["dedicated_to_category"])                
                app_perm.dedicated_to_category = category
                app_perm.save()
            else:
                app_perm.dedicated_to_category = None
                app_perm.save()
                
            if request.POST["dedicated_to_sub_category"] != "":
                sub_category = Category.objects.get(pk = request.POST["dedicated_to_sub_category"])
                app_perm.dedicated_to_sub_category = sub_category
                app_perm.save()
            else:
                app_perm.dedicated_to_sub_category = None
                app_perm.save()
            
            if request.POST["dedicated_to_brand"] != "":
                brand = Brand.objects.get(pk = request.POST["dedicated_to_brand"])
                app_perm.dedicated_to_brand = brand
                app_perm.save()
            else:
                app_perm.dedicated_to_brand = None
                app_perm.save()
                
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
    if request.GET["cat_id"] != "":
        sub_cats = records_helper.SubCategoryList(request.GET["cat_id"])
        
        html = ['<option value="''">Any</option>']
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
            
            if request.POST["dedicated_to_category"] != "":
                category = Category.objects.get(pk = request.POST["dedicated_to_category"])                
                app_perm.dedicated_to_category = category
                app_perm.save()
            else:
                app_perm.dedicated_to_category = None
                app_perm.save()
                
            if request.POST["dedicated_to_sub_category"] != "":
                sub_category = Category.objects.get(pk = request.POST["dedicated_to_sub_category"])
                app_perm.dedicated_to_sub_category = sub_category
                app_perm.save()
            else:
                app_perm.dedicated_to_sub_category = None
                app_perm.save()
            
            if request.POST["dedicated_to_brand"] != "":
                brand = Brand.objects.get(pk = request.POST["dedicated_to_brand"])
                app_perm.dedicated_to_brand = brand
                app_perm.save()
            else:
                app_perm.dedicated_to_brand = None
                app_perm.save()
                        
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
                'js_files' : self.js_files,
            })

        

#=========================================================================================
#   RECORD MANAGEMENT
#=========================================================================================

class RecordManagement(View):
    template_name = 'app/record_management/index.html'
    msg = ''
    js_files = ['app_files/records_management.js']

    def get(self, request, *args, **kwargs):   

        page = request.GET.get('page',1)
        records_per_page = request.GET.get('per_page',None)
        load_file = request.GET.get('load_file', None) 
        
        #
        #   filters
        #
        
        active = request.GET.get('active', None)
        assigned = request.GET.get('assigned',None)
        cate = request.GET.get('cate', None)
        sub_cat = request.GET.get('sub_cat', None)
        brand = request.GET.get('brand', None)
        
        if(active is None and assigned is None and cate is None and sub_cat is None and brand is None):
            kwargs = None
        else:
            kwargs = {
                "active" : active,
                "assigned" : assigned,
                "cate" : cate,
                "sub_cat" : sub_cat,
                "brand" : brand,
            }
        
        file_ins, records = records_helper.RecordsList(page, records_per_page, load_file, kwargs)

        records_file_list = records_helper.RecordsFileList()

        context = {
            "file_submission_form" : FileSubmissionForm(),
            "records" : {},
            "file_ins" : '',
            "records_file_list" : records_file_list,
            "js_files" : self.js_files,
            "user_list" : user_helper.StaffList(),
            'category_list' : records_helper.CategoryList(),
            'sub_category_list' : records_helper.SubCategoryList(),
            'brand_list' : records_helper.BrandList(),
            'error_msg': None, 
        }

        if load_file is not None:
            context["url_ext"] = "&load_file="+load_file
        else:
            context["load_file"] = ""

        if file_ins is not False:
            context["records"] = records
            context["file_ins"] = file_ins.id

        return render(request, self.template_name, context)     


    def post(self, request, *args, **kwargs):

        file_submission_form = FileSubmissionForm(request.POST or None, request.FILES or None)

        if file_submission_form.is_valid():
            ins = file_submission_form.save()

            rec_msg = records_helper.insert_into_db(ins, ins.filename())
            
            if ins.is_active:
                self.msg = "File Uploaded Successfully and loaded"
            else:
                self.msg = "File Uploaded Successfully, but did not load the data since the file uploaded is inactive. \
                <br><br/>Please activate the file to show it in the 'Select Records File'. If its the latest and its inactive \
                file then the data will be automatically loaded from the previously uploaded file, else you have to load the \
                data by selecting the latest file from 'Select Records File' and then click the 'Load Data' button."
            
            messages.add_message(request, messages.INFO, self.msg + "<br>"+rec_msg)

            return redirect('/record-management/',)

        self.msg = file_submission_form.errors  
        return render(request, self.template_name, {
            "file_submission_form" : FileSubmissionForm(),
            "error_msg" : self.msg,
        })
    
    
#=========================================================================================
# DELETE FILE PERMANENTLY WITH RECORDS
#=========================================================================================     

def delete_file_data(request):
    file_ins = request.GET["file_ins"]
    
    try:
        FileSubmission.objects.get(pk = file_ins).delete()
    except:
        pass
    finally:
        return HttpResponse('1')
 
#=========================================================================================
# ACTIVATE RECORDS
#=========================================================================================    
def activate_records(request):
    records = request.POST.getlist('case[]')  
    opt = request.POST['opt']
    
    if len(records) > 0:
        records_helper.RecordsStatus(records, opt)
        
    return HttpResponse('1')
    

#=========================================================================================
# AUTO ASSIGN RECORDS
#=========================================================================================    
def auto_assign(request):
    opt = request.POST.get('opt',False)
    file_ins = request.POST.get('file_ins',None)
    auto_assign_staff = request.POST.getlist('auto_assign_staff', list())
    
    if opt == '0':
        opt = False
    else:
        opt = True
        
    if '0' in auto_assign_staff:
        auto_assign_staff = [0]

    if file_ins is not None and opt:
        records_helper.AutoAssignRecords(file_ins, opt, auto_assign_staff)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/record-management/'))


#=========================================================================================
# STAFF/USER RECORD
#=========================================================================================  
class StaffRecord(View):

    template_name = 'app/staff_section/index.html'
    context = {}
    context["js_files"] = ['app_files/staff_records.js']
    
    def get(self, request, *args, **kwargs):
        
        if not kwargs:
            
            record_fetch = records_helper.GetRecord(request.user)
        
            self.context["records"] = record_fetch
            
        return render(request, self.template_name, self.context)      
        
        
    def post(self, request, *args, **kwargs):
        record = RecordsManagement.objects.get(pk = request.POST["record_id"])
        
        record.contact_person = request.POST["contact_person"]
        record.contact_number = request.POST["contact_number"]
        record.email = request.POST["email"]
        record.remarks = request.POST["remarks"]
        record.remark_added_on = timezone.now()
        record.disposition = request.POST["disposition"]
        
        record.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/staff-record/'))

    
#=========================================================================================
# SET RECORD AS COMPLETED
#=========================================================================================  
def set_completed(request):

    status = False
    rec_id = request.GET["rec_id"]
    
    if request.GET["status"] == '1':
        status = True
    
    try:
        rec = RecordsManagement.objects.get(pk = rec_id) 
        rec.is_completed = status
        rec.save()
    except:
        pass
    return HttpResponse('')
    

#=========================================================================================
# GET RECORD DETAILS
#=========================================================================================     
def get_record_details(request):

    rec_id = request.GET['rec_id']
    rec = RecordsManagement.objects.filter(pk = rec_id).values('id','contact_person', 'contact_number', 
            'email', 'disposition', 'remarks')
    
    return JsonResponse({'rec':list(rec)})
    
#=========================================================================================     
# 
#=========================================================================================     
    
    
    
    
    