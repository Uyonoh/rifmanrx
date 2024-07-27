from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(BusinessMonth)
admin.site.register(Credit)
admin.site.register(Debit)
admin.site.register(Sale)
admin.site.register(Purchase)