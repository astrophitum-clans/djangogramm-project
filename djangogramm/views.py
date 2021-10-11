from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, ListView
from django.core.signing import BadSignature

from djangogramm.utilities import signer
from djangogramm.forms import LoginForm, SignUpForm, UserProfileForm, PostCreateForm
from djangogramm.models import DgUser, DgPost


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


# Djangogramm views

class DgPostListView(LoginRequiredMixin, ListView):
    """Index page"""
    model = DgPost
    template_name = 'djangogramm/index.html'

    def get_queryset(self):
        return DgPost.objects.select_related('dg_user')


class DgPostCreateView(LoginRequiredMixin, CreateView):
    """Add post page"""
    template_name = 'djangogramm/post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('djangogramm:index')

    def form_valid(self, form):
        form.instance.dg_user = self.request.user
        return super().form_valid(form)
