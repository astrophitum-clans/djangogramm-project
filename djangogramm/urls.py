from django.urls import path

from .views import (DgUserLoginView, DgUserLogoutView, DgUserSignUpView, index, DgUserSignUpDoneView, DgUserProfileView,
                    user_activate)

app_name = 'djangogramm'

urlpatterns = [
    # user accounts
    path('accounts/login/', DgUserLoginView.as_view(), name='login'),
    path('accounts/logout/', DgUserLogoutView.as_view(), name='logout'),
    path('accounts/signup/done/', DgUserSignUpDoneView.as_view(), name='signup_done'),
    path('accounts/signup/', DgUserSignUpView.as_view(), name='signup'),
    path('accounts/activate/<str:sign>/', user_activate, name='activate'),
    path('accounts/profile/', DgUserProfileView.as_view(), name='profile'),
    # the djangogramm
    path('', index, name='index'),
]
