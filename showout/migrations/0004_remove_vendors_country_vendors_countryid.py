# Generated by Django 5.0.1 on 2024-02-26 16:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0003_remove_category_id_remove_country_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendors",
            name="country",
        ),
        migrations.AddField(
            model_name="vendors",
            name="countryId",
            field=models.IntegerField(default=1),
        ),
    ]
