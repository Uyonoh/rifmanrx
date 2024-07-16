from django.urls import path, include
from .views import signup

app_name = "users"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup", signup, name="signup"),
]