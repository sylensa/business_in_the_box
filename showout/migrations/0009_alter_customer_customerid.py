# Generated by Django 5.0.1 on 2024-02-19 21:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0008_alter_customer_customerid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="customerId",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]