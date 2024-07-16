from django.urls import path, include

app_name = "users"

urlpatterns = [
    path("login/", include("django.contrib.auth.urls")),
]