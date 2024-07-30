from django.urls import path, include
from .views import view_drugs, view_drug, add_drug, sell, restock, edit, add_csv

app_name = "drugs"

urlpatterns = [
    path("view/", view_drugs, name="view"),
    path("view/<int:pk>", view_drug, name="view-drug"),
    path("add/", add_drug, name="add"),
    path("sell/<int:pk>", sell, name="sell"),
    path("restock/<int:pk>", restock, name="restock"),
    path("edit/<int:pk>", edit, name="edit"),
    path("add-csv", add_csv, name="add-csv"),
]