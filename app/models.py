from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    pass


@receiver(post_save, sender=User)
def create_app_permission(sender, instance, created, **kwargs):
    if created:
        AppPermission.objects.create(user=instance)


#*********************************************************************
# 
#*********************************************************************



