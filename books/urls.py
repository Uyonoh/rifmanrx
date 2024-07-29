from django.urls import path, include
from .views import view_month, view_sales

app_name = "books"

urlpatterns = [
    path("", view_month, name="view"),
    path("<int:pk>/sales/",  view_sales, name="sales"),
    # path("credits"),
    # path("debits"),
    # path("month"),
]