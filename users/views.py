from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView

# Create your views here.

def signup(request):
    return render(request, "users/signup.html", {})