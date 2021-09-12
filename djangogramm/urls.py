from django.urls import path

from .views import DgUserLoginView, profile, DgUserLogoutView

urlpatterns = [
    path('accounts/login/', DgUserLoginView.as_view(), name='login'),
    path('accounts/logout/', DgUserLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile')
]