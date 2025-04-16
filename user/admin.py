from django.contrib import admin

from .models import Users, Purchases, Register

# Register your models here.
admin.site.register(Users)
admin.site.register(Purchases)
admin.site.register(Register)