# Generated by Django 5.0.1 on 2024-03-03 11:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("showout", "0022_rename_generid_gender_genderid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vendors",
            old_name="generId",
            new_name="genderId",
        ),
    ]