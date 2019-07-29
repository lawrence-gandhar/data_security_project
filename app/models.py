from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, db_index = True, on_delete = models.CASCADE)
    profile_pic = models.TextField(null = True, blank = True,) 
    phone = models.CharField(max_length = 250, null = True, blank = True,)
    
    class Meta:
        db_table = 'user_profile'


class AppPermission(models.Model):
    user = models.OneToOneField(User, db_index = True, on_delete = models.CASCADE)
    record_access_size = models.BigIntegerField(db_index = True, default = 0,)
    full_access = models.BooleanField(db_index = True, default = False,)

    class Meta:
        db_table = 'user_app_permissions'
    pass


#*********************************************************************
# SIGNALS
#*********************************************************************

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_app_permission(sender, instance, created, **kwargs):
    if created:
        AppPermission.objects.create(user=instance)
