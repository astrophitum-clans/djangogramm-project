from cloudinary.models import CloudinaryField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from .utilities import get_timestamp_path


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
    avatar = CloudinaryField('image', blank=True, null=True)

    followers = models.ManyToManyField('self', symmetrical=False, blank=True)

    objects = DgUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def following(self):
        """Return following users"""
        return DgUser.objects.filter(followers=self)

    @property
    def fullname(self):
        fullname = f'{self.first_name} {self.last_name}'
        return fullname if len(fullname) > 1 else None

    @property
    def get_name(self):
        """Return user name for views"""
        return self.fullname or self.username or self.email.split('@')[0]

    @property
    def count_followers(self):
        """Return followers count"""
        return self.followers.count()

    @property
    def count_following(self):
        """Return following count"""
        return self.following.count()

    def is_follower(self, user):
        """Return True if user is follower of this"""
        return user in self.followers.all()


class DgPost(models.Model):
    """Djangogramm post model"""
    dg_user = models.ForeignKey(DgUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='title')
    desc = models.TextField(blank=True, null=True, verbose_name='description')
    image = CloudinaryField('image', blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='publication date')

    def __str__(self):
        return self.title

    def get_total_likes(self):
        """Return number of likes"""
        return self.likes.users.count() if self.likes.users.count() > 0 else '0'

    class Meta:
        ordering = ['-pub_date']


class Like(models.Model):
    """Likes model"""
    post = models.OneToOneField(DgPost, related_name='likes', on_delete=models.CASCADE)
    users = models.ManyToManyField(DgUser, related_name='like_users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
