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

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
