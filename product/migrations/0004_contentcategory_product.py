# Generated by Django 5.0.7 on 2024-09-04 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentcategory',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]
