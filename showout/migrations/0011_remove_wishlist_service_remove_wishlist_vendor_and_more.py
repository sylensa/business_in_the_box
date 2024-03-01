# Generated by Django 5.0.1 on 2024-03-01 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0010_vendorservices_rating_alter_vendorservices_vendor_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wishlist",
            name="service",
        ),
        migrations.RemoveField(
            model_name="wishlist",
            name="vendor",
        ),
        migrations.AddField(
            model_name="wishlist",
            name="vendorService",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="showout.vendorservices",
            ),
        ),
        migrations.AlterField(
            model_name="reviewvendoreservices",
            name="reviewVendoreServicesId",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="wishlist",
            name="wishListId",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
