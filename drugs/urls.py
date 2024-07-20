from django.urls import path, include
from .views import view_drugs, add_drug

app_name = "drugs"

urlpatterns = [
    path("view/", view_drugs, name="view"),
    path("add/", add_drug, name="add"),
]