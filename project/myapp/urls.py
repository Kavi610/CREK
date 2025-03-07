from django.urls import path
from . import views

urlpatterns = [
    path("create-doc/", views.CreateGoogleDoc.as_view(), name="create-google-doc"),
    path("index/", views.home, name="home"),
]
