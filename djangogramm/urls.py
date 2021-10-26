from django.urls import path

from .views import (DgUserLoginView, DgUserLogoutView, DgUserSignUpView, DgUserSignUpDoneView, DgUserProfileView,
                    user_activate, DgPostListView, DgPostCreateView, DgNewsListView, follow, like)

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
    path('', DgPostListView.as_view(), name='index'),
    path('posts/create/', DgPostCreateView.as_view(), name='post_create'),
    path('news/', DgNewsListView.as_view(), name='news'),
    path('follow/<int:dg_user_id>/', follow, name='follow'),
    path('posts/<int:post_id>/like/', like, name='like'),

]
