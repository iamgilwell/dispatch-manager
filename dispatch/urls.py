from django.urls import path
from dispatch.views import DispatchListView

app_name = "dispatch"

urlpatterns = [
    path('<str:slug>/', DispatchListView.as_view(), name='index')
]
