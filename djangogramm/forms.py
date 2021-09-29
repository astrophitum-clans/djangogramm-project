from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm

from djangogramm.apps import user_signup


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text='Required.',
        widget=forms.EmailInput()  # attrs={'autofocus': 'autofocus'}
    )

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_signup.send(SignUpForm, instance=user)
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'bio', 'avatar')
