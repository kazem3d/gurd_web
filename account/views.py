from django.shortcuts import render
from django.contrib.auth.views import LoginView,LogoutView

# Create your views here.

class Login(LoginView):
    pass

class Logout(LogoutView):
    pass