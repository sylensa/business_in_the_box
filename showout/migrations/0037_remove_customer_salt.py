# Generated by Django 5.0.1 on 2024-03-18 15:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0036_customer_salt"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="salt",
        ),
    ]
