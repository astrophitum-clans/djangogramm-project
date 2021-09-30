from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm

from djangogramm.apps import user_signup


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

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'bio', 'avatar')
