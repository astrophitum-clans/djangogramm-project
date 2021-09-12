from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render


# Create your views here.

class DgUserLoginView(LoginView):
    template_name = 'djangogramm/login.html'


@login_required
def profile(request):
    return render(request, 'djangogramm/profile.html')


class DgUserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'djangogramm/logout.html'