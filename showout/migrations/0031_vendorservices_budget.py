# Generated by Django 5.0.1 on 2024-03-08 23:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0030_remove_services_description_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendorservices",
            name="budget",
            field=models.FloatField(default=0.0),
        ),
    ]
