from django.contrib import admin
from .models import Item, CustomUser

admin.site.register(CustomUser)
admin.site.register(Item)