from django.db import models
from django.contrib.auth import get_user
from django.contrib.auth.models import User

# Create your models here.

class PharmUser(User):
    """ A pharmacy user model """

    def __str__(self) -> str:
        return f"User: {self.username}"
    