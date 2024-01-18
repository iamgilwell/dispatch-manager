from django.shortcuts import get_object_or_404, render

from django.views.generic.list import ListView
from dispatch.models import Item, ItemTracker

class DispatchListView(ListView):
    template_name = "dispatch/index.html"
    model = ItemTracker

    def get_object(self):
        return get_object_or_404(Item, slug=self.kwargs['slug'])

    def get_queryset(self):
      return ItemTracker.objects.filter(item=self.get_object())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object"] = self.get_object()
        return context