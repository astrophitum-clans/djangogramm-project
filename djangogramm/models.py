from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class DgUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a user with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        # a user is not active and not activated before email confirmation
        user.is_active = False
        user.is_activated = False

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        # a superuser is always active and not required to activation.
        user.is_active = True
        user.is_activated = True
        user.save(using=self._db)
        return user


class DgUser(AbstractUser):
    """Djangogramm user model"""
    username = models.CharField(blank=True, max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_activated = models.BooleanField(default=False, db_index=True, verbose_name='is activated')
    bio = models.TextField(blank=True, null=True, verbose_name='biography')
    avatar = models.ImageField(blank=True, null=True, verbose_name='user avatar')

    objects = DgUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
