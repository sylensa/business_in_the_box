# Generated by Django 5.0.1 on 2024-03-08 23:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0029_alter_vendors_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="services",
            name="description",
        ),
        migrations.AddField(
            model_name="vendorservices",
            name="description",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
