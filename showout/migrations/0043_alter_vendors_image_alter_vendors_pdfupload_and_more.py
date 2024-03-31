# Generated by Django 5.0.1 on 2024-03-23 10:26

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0042_merge_20240323_1017"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendors",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location="/Users/mac/Desktop/Django/business_in_the_box/static/images"
                ),
                upload_to="",
            ),
        ),
        migrations.AlterField(
            model_name="vendors",
            name="pdfUpload",
            field=models.FileField(
                blank=True,
                null=True,
                storage=django.core.files.storage.FileSystemStorage(
                    location="/Users/mac/Desktop/Django/business_in_the_box/static/images"
                ),
                upload_to="",
            ),
        ),
        migrations.AlterField(
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