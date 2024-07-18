from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django .contrib.auth import get_user
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from .forms import PharmUserForm
from django.contrib.auth.hashers import make_password

# Create your views here.

# def login_auth(request):


def signup(request):
    """ Create a new user if user does not previously exist   """
    
    if request.method == "POST":
        form = PharmUserForm(request.POST)
        
        if form.is_valid():
            form.instance.password = make_password(form.instance.password)
            print(form)
            form.save()
        else:
            print(form.errors)
            return render(request, "users/signup.html", {})

    return render(request, "users/signup.html", {})