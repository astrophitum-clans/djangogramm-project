from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from django.core.signing import BadSignature

from djangogramm.utilities import signer
from djangogramm.forms import LoginForm, SignUpForm, UserProfileForm
from djangogramm.models import DgUser


@login_required
def index(request):
    return HttpResponse('<h2>This is DjangoGramm</h2>')

# User views

class DgUserLoginView(LoginView):
    """User login view"""
    form_class = LoginForm
    template_name = 'djangogramm/login.html'
    success_url = reverse_lazy('djangogramm:index')


class DgUserLogoutView(LogoutView):
    """User logout view"""
    template_name = 'djangogramm/logout.html'


class DgUserSignUpView(CreateView):
    """User signup view"""
    model = DgUser
    form_class = SignUpForm
    template_name = 'djangogramm/signup.html'
    success_url = reverse_lazy('djangogramm:signup_done')


class DgUserSignUpDoneView(TemplateView):
    """User signup done view"""
    template_name = 'djangogramm/signup_done.html'


def user_activate(request, sign):
    """User activation view. Login and redirect to user profile page after successfully activation"""
    try:
        email = signer.unsign(sign)
    except BadSignature:
        return render(request, 'djangogramm/bad_signature.html')
    user = get_object_or_404(DgUser, email=email)
    if user.is_activated:
        return render(request, 'djangogramm/user_is_activated.html')
    else:
        user.is_active = True
        user.is_activated = True
        user.save()
        login(request, user)
        return redirect('djangogramm:profile')


class DgUserProfileView(LoginRequiredMixin, UpdateView):
    """User update profile view"""
    template_name = 'djangogramm/user_profile.html'
    model = DgUser
    form_class = UserProfileForm
    success_url = reverse_lazy('djangogramm:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)
