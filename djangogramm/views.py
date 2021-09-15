from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from djangogramm.forms import LoginForm, SignupForm, UserProfileForm
from djangogramm.models import DgUser


@login_required
def index(request):
    return HttpResponse('<h2>This is DjangoGramm</h2>')


class DgUserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'djangogramm/login.html'
    success_url = reverse_lazy('djangogramm:index')


class DgUserLogoutView(LogoutView):
    template_name = 'djangogramm/logout.html'


class DgUserSignupView(LoginRequiredMixin, CreateView):
    form_class = SignupForm
    template_name = 'djangogramm/signup.html'
    success_url = reverse_lazy('djangogramm:login')


class DgUserProfileView(LoginRequiredMixin, UpdateView):
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

