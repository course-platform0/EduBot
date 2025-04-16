from django.db import models

from product.models import Product


# Create your models here.


class Register(models.Model):
    user_email = models.EmailField(null=True)
    user_phone = models.CharField(max_length=15, null=True)
    code = models.PositiveIntegerField()
    date_register = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user_email


class Users(models.Model):
    user_name = models.CharField(max_length=100, unique=True, null=True)
    chat_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    user_email = models.CharField(max_length=150, unique=True, null=True)
    user_phone = models.CharField(max_length=15, unique=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user_email


class Purchases(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.user_email
