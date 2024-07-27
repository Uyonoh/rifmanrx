from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

def view_months(request):
    return render(request, "books/view.html")