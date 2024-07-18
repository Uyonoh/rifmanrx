from django import forms
from .models import PharmUser
from django.contrib.auth.models import User

class PharmUserForm(forms.ModelForm):
    """ Base form for regular users """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password"]