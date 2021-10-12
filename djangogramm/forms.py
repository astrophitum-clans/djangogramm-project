from cloudinary.forms import CloudinaryFileField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm

from djangogramm.apps import user_signup
from djangogramm.models import DgPost


class SignUpForm(UserCreationForm):
    """User signup form"""
    email = forms.EmailField(
        required=True,
        help_text='Required.',
        widget=forms.EmailInput()
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        # set to False before activation
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        # send email confirmation signal
        user_signup.send(SignUpForm, instance=user)

        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    """User login form"""
    username = forms.EmailField(label='Email')


class UserProfileForm(ModelForm):
    """User profile form"""
    email = forms.EmailField(
        disabled=True
    )
    avatar = CloudinaryFileField(
        options={
            'tags': "user_avatar",
            'crop': 'fill', 'width': 256, 'height': 256,
            'folder': 'media/avatars/',
            'eager': [{'crop': 'fill', 'height': 100, 'width': 100}]
        },
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'bio', 'avatar')


class PostCreateForm(ModelForm):
    """Create post form"""
    image = CloudinaryFileField(
        options={
            'tags': "post_image",
            'crop': 'fill', 'width': 960,
            'folder': 'media/images/'
        },
        required=False
    )

    class Meta:
        model = DgPost
        fields = ('title', 'desc', 'image')
