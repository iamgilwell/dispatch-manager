from django.shortcuts import render

from django.views.generic.list import ListView
from dispatch.models import Item

class HomeView(ListView):
    template_name = "home/index.html"
    model = Item