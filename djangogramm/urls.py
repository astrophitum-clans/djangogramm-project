from django.urls import path

from .views import DgUserLoginView

urlpatterns = [
    path('accounts/login/', DgUserLoginView.as_view(), name='login'),
]