from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os, sys


#*********************************************************************
# MODEL- USER PROFILE
#*********************************************************************

class UserProfile(models.Model):
    user = models.OneToOneField(User, db_index = True, on_delete = models.CASCADE, related_name = 'profile')
    profile_pic = models.ImageField(upload_to='profiles/', null = True, blank = True, )
    phone = models.CharField(max_length = 250, null = True, blank = True,)
    
    def __str__(self):
        return "{0} {1}".format((self.user.first_name).upper(), (self.user.last_name).upper())

    class Meta:
        db_table = 'user_profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


#*********************************************************************
# MODEL - USER RECORD PERMISSIONS
#*********************************************************************

class AppPermission(models.Model):
    user = models.OneToOneField(User, db_index = True, on_delete = models.CASCADE, related_name = 'app_permissions')
    record_access_size = models.BigIntegerField(db_index = True, default = 0,)
    full_access = models.BooleanField(db_index = True, default = False,)
    read_only_mode = models.BooleanField(db_index = True, default = True,)

    def __str__(self):
        return "{0} {1}".format((self.user.first_name).upper(), (self.user.last_name).upper())

    class Meta:
        db_table = 'user_app_permissions'
    


@receiver(post_save, sender=User)
def create_app_permission(sender, instance, created, **kwargs):
    if created:
        AppPermission.objects.create(user=instance)


#*********************************************************************
# MODEL - FILE SUBMISSIONS 
#*********************************************************************

class FileSubmission(models.Model):

    record_file_name = models.FileField(upload_to='records/', blank = False, null = False)    
    is_active = models.BooleanField(db_index = True, default = True,)
    uploaded_on = models.DateTimeField(auto_now_add = True, db_index = True)

    def __str__(self):
        return "{0}".format(self.record_file_name)

    def filename(self):
        return "/records/"+os.path.basename(self.record_file_name.name)

    class Meta:
        db_table = 'file_submission_tbl'
    

#*********************************************************************
# MODEL - CATEGORY 
#*********************************************************************

class Category(models.Model):

    category_name = models.CharField(max_length = 250, blank = False, null = False, unique = True,)
    category_is_parent = models.BooleanField(db_index = True, default = True)
    category_parent_id = models.ForeignKey('self', db_index = True, on_delete = models.SET_NULL, null = True, blank = True,)
    is_active = models.BooleanField(default = True, db_index = True)

    def __str__(self):
        return "{0}".format(self.category_name.title())

    class Meta:
        db_table = 'category_tbl'
    


#*********************************************************************
# MODEL - BRANDS 
#*********************************************************************

class Brand(models.Model):
    brand_name = models.CharField(max_length = 250, unique = True, blank = False, null = False,)
    is_active = models.BooleanField(db_index = True, default = True)
    
    def __str__(self):
        return "{0}".format(self.brand_name)

    class Meta:
        db_table = 'brands_tbl'


#*********************************************************************
# MODEL - RECORDS MANAGEMENT 
#*********************************************************************

class RecordsManagement(models.Model):
    record_file = models.ForeignKey(FileSubmission, null = True, blank = True, on_delete = models.SET_NULL, db_index = True,)
    is_active = models.BooleanField(db_index = True, default = True)
    category = models.ForeignKey(Category, blank = True, null = True, db_index = True, on_delete = models.SET_NULL, related_name = 'record_category') 
    sub_category = models.ForeignKey(Category, blank =True, null = True, db_index = True, on_delete = models.SET_NULL, related_name = 'record_sub_category')
    brand = models.ForeignKey(Brand, db_index = True, blank = True, null = True, on_delete = models.SET_NULL) 
    contact_person = models.CharField(max_length = 250, blank = True, null = True, )
    contact_number = models.CharField(max_length = 250, blank = True, null = True, )
    email = models.CharField(max_length = 250, blank = True, null = True, )
    is_assigned = models.BooleanField(default = False, db_index = True,)
    assigned_to = models.ForeignKey(User, db_index = True, null = True, on_delete = models.SET_NULL,)
    assigned_on = models.DateTimeField(null = True, db_index = True,)
    remarks = models.TextField(null = True, blank = True, )
    remark_added_on = models.DateTimeField(null = True, db_index = True,)
    disposition = models.IntegerField(default = 0, db_index = True,)

    class Meta:
        db_table = 'records_tbl'
        
        