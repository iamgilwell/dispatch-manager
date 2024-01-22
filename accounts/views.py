from django.shortcuts import render
from django.views.generic.list import ListView
from django.contrib.auth import  login as user_login, authenticate, logout, get_user_model

User = get_user_model()

class AccountListView(ListView):
    template_name = "dispatch/index.html"
    model = User
