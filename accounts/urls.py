from django.urls import path

from accounts.views import AccountListView

app_name = "accounts"

urlpatterns = [
    path('', AccountListView.as_view(), name='index')
]