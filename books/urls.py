from django.urls import path, include
from .views import view_months, view_month, view_sales, view_purchases, view_credits, view_debits

app_name = "books"

urlpatterns = [
    path("", view_months, name="view"),
    path("<int:pk>/", view_month, name="view-month"),
    path("<int:pk>/sales/",  view_sales, name="sales"),
    path("<int:pk>/purchases/",  view_purchases, name="purchases"),
    path("<int:pk>/debits/",  view_debits, name="debits"),
    path("<int:pk>/credits/",  view_credits, name="credits"),
]