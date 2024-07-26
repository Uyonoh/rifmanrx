from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Drug)
admin.site.register(Tablet)
admin.site.register(Suspension)
admin.site.register(Injectible)
admin.site.register(Sale)