# Generated by Django 5.0.1 on 2024-03-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0032_remove_vendors_facebook_remove_vendors_instagram_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="address",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]