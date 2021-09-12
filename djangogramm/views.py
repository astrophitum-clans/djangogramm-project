from django.contrib.auth.views import LoginView
from django.shortcuts import render


# Create your views here.

class DgUserLoginView(LoginView):
    template_name = 'djangogramm/login.html'
