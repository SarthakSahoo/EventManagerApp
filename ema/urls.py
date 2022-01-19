# Importing the libraries
from django.urls import path

from ema import views

# URL patterns for accessing the frontend
urlpatterns=[
    path("login", views.LoginUser.as_view(), name='login'),
    path("logout", views.LogoutView.as_view(), name='logout'),
    path("register", views.RegisterUser.as_view(), name='register-user'),
    path("sendloginotp", views.LoginWithOTP.as_view(), name='login-with-otp'),
    path("verify", views.VerifyUser.as_view(), name='verify-user')
]
