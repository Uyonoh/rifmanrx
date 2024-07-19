from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django .contrib.auth import get_user
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth import get_user
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
            form.save()
            return HttpResponseRedirect(reverse("users:login"))
        else:
            print(form.errors.items())
            return render(request, "users/signup.html", {"form": form})
        
    return render(request, "users/signup.html", {})

def profile(request):
    user = get_user(request)
    
    if isinstance(user, AnonymousUser):
        return HttpResponseRedirect(reverse("users:login"))
    else:
        user_dict = user.__dict__.copy()
        del user_dict["_state"]
        del user_dict["is_active"]
        del user_dict["password"]
        return render(request, "users/profile.html", {"user": user_dict})