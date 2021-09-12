from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class DgUser(AbstractUser):
    """extended User model"""
    is_activated = models.BooleanField(verbose_name='Is user activated', default=False, db_index=True)
    bio = models.TextField(verbose_name='biography', null=True, blank=True)
    avatar = models.ImageField(verbose_name='user avatar', null=True, blank=True)
