from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    logo = models.CharField(max_length=300)
    description = models.TextField()
    title = models.CharField(max_length=150)
    video_intro = models.CharField(max_length=300)
    content_description = models.TextField()
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ContentCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class ProductContent(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content_category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    cover_image = models.CharField(max_length=300)
    video_link = models.CharField(max_length=300)

    def __str__(self):
        return self.name
