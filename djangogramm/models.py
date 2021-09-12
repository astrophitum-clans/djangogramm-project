from django.contrib.auth.models import AbstractUser
from django.db import models


class DgUser(AbstractUser):
    """extended User model"""
    is_activated = models.BooleanField(default=False, db_index=True, verbose_name='is user activated')
    bio = models.TextField(blank=True, null=True, verbose_name='biography')
    avatar = models.ImageField(blank=True, null=True, verbose_name='user avatar')
    email = models.EmailField(blank=True, unique=True, max_length=254, verbose_name='email address')
