from django.urls import path

from .views import DgUserLoginView, DgUserLogoutView, DgUserSignupView, index, DgUserProfileView

app_name = 'djangogramm'

urlpatterns = [
    path('accounts/login/', DgUserLoginView.as_view(), name='login'),
    path('accounts/logout/', DgUserLogoutView.as_view(), name='logout'),
    path('accounts/register/', DgUserSignupView.as_view(), name='register'),
    path('accounts/profile/', DgUserProfileView.as_view(), name='profile'),
    path('', index, name='index'),
]
