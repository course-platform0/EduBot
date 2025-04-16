from django.db import models

from product.models import Product, ContentCategory
from user.models import Users


# Create your models here.
class UserVisit(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content_category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
