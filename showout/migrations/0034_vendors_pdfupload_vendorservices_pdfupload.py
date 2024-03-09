# Generated by Django 5.0.1 on 2024-03-09 17:14

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0033_customer_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendors",
            name="pdfUpload",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location="/Users/mac/Desktop/Django/business_in_the_box/static/images"
                ),
                upload_to="",
            ),
        ),
        migrations.AddField(
            model_name="vendorservices",
            name="pdfUpload",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location="/Users/mac/Desktop/Django/business_in_the_box/static/images"
                ),
                upload_to="",
            ),
        ),
    ]
