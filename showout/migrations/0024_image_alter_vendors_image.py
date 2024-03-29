# Generated by Django 5.0.1 on 2024-03-03 13:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0023_rename_generid_vendors_genderid"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="images/")),
            ],
        ),
        migrations.AlterField(
            model_name="vendors",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
