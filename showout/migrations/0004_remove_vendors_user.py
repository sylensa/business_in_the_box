# Generated by Django 5.0.1 on 2024-02-18 11:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0003_remove_category_id_remove_country_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendors",
            name="user",
        ),
    ]
