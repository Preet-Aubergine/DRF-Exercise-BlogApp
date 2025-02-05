from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# user profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank=True,null=True, upload_to='profile_pics/')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.user.email