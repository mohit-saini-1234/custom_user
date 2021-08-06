from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path as url
from django.contrib.auth import views as auth_views
from Accounts.views import UseRegister ,UserProfile ,UpdateUserView,DeleteUserView ,AssignUserRole, UserLogin , ChangePasswordView , TempPassword , ForgotPassword


urlpatterns = [
    url(r'^reg/$', UseRegister.as_view()),
    url(r'^profile/$', UserProfile.as_view()),
    url(r'^mail/$', ForgotPassword.as_view()),
    url(r'^login/$', UserLogin.as_view()),
    url(r'^update/$', UpdateUserView.as_view()),
    path('delete/<int:pk>/', DeleteUserView.as_view()),
    path('role/<int:pk>/', AssignUserRole.as_view()),
    url(r'^set_pass/$', TempPassword.as_view()),
    url(r'^password/$', ChangePasswordView.as_view()),]
    