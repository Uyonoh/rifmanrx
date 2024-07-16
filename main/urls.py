from django.urls import path, include
from .views import *

app_name = "main"

urlpatterns = [
    path("", home, name="home"),
    path("contact/", contact, name="contact"),
    path("about/", about, name="about"),
]