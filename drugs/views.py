from django.shortcuts import render

# Create your views here.

def view_drugs(request):
    return render(request, "drugs/view-drugs.html", {})


def add_drug(request):
    return render(request, "drugs/add-drug.html", {})