from django.urls import path, include
from .views import signup, profile

app_name = "users"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    # path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
]