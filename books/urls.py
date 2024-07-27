from django.urls import path, include
from .views import view_month

app_name = "books"

urlpatterns = [
    path("", view_month, name="view"),
    # path("credits"),
    # path("debits"),
    # path("month"),
]