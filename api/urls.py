from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.CreateAccountView.as_view(), name="account_create"),
]
