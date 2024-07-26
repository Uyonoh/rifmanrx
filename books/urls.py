from django.urls import path, include
from .views import view_months

app_name = "books"

urlpatterns = [
    path("", view_months, name="view"),
    # path("credits"),
    # path("debits"),
    # path("month"),
]