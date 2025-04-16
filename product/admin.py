from django.contrib import admin

from .models import Product, ProductContent, ContentCategory

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductContent)
admin.site.register(ContentCategory)