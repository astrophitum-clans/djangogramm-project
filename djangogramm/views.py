from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Exists, OuterRef
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

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        followers = DgPost.objects.filter(id=OuterRef('pk'), dg_user__followers=self.user)
        likes = DgPost.objects.filter(id=OuterRef('pk'), likes__user=self.user)
        posts = DgPost.objects.prefetch_related('dg_user').annotate(is_follower=Exists(followers)).annotate(
            is_like=Exists(likes))
        return posts


class DgPostCreateView(LoginRequiredMixin, CreateView):
    """Add post page"""
    template_name = 'djangogramm/post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('djangogramm:index')

    def form_valid(self, form):
        form.instance.dg_user = self.request.user
        return super().form_valid(form)


class DgNewsListView(LoginRequiredMixin, ListView):
    """News list page"""
    model = DgPost
    template_name = 'djangogramm/index.html'

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        return super().setup(request, *args, **kwargs)

    def get_queryset(self):
        followers = DgPost.objects.filter(id=OuterRef('pk'), dg_user__followers=self.user)
        likes = DgPost.objects.filter(id=OuterRef('pk'), likes__user=self.user)
        posts = DgPost.objects.filter(dg_user__in=self.user.following).prefetch_related('dg_user').annotate(
            is_follower=Exists(followers)).annotate(is_like=Exists(likes))
        return posts


@login_required
def follow(request, dg_user_id):
    """follow/unfollow functionality"""
    if request.method == 'POST':
        following_user = get_object_or_404(DgUser, pk=dg_user_id)
        if request.POST['isfollow'] == 'follow' and not following_user.followers.filter(id=request.user.id).exists():
            following_user.followers.add(request.user)
        elif request.POST['isfollow'] == 'unfollow':
            following_user.followers.remove(request.user)
        return redirect(request.POST.get('next', '/'))


@login_required
def like(request, post_id):
    """like/unlike functionality"""
    if request.method == 'POST':
        post = get_object_or_404(DgPost, pk=post_id)
        if request.POST['islike'] == 'like' and not post.likes.filter(user=request.user).exists():
            post.likes.create(user=request.user)
        elif request.POST['islike'] == 'unlike':
            post.likes.filter(user=request.user).delete()
        return redirect(request.POST.get('next', '/'))
