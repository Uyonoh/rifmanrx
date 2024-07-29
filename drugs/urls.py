from django.urls import path, include
from .views import view_drugs, view_drug, add_drug, sell, restock, edit, add_csv, search_drugs, print_stock

app_name = "drugs"

urlpatterns = [
    path("view/", view_drugs, name="view"),
    path("view/<int:pk>", view_drug, name="view-drug"),
    path("add/", add_drug, name="add"),
    path("add-csv", add_csv, name="add-csv"),
    path("sell/<int:pk>", sell, name="sell"),
    path("restock/<int:pk>", restock, name="restock"),
    path("edit/<int:pk>", edit, name="edit"),
    path("search/", search_drugs, name="search"),
    path("print/", print_stock, name="print"),
]