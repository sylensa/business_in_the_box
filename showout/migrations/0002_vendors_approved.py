# Generated by Django 5.0.1 on 2024-02-15 09:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="vendors",
            name="approved",
            field=models.BooleanField(default=False),
        ),
    ]