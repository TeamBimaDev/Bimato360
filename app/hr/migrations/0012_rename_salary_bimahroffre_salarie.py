# Generated by Django 5.0.6 on 2024-07-03 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0011_alter_bimahroffre_salary"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bimahroffre",
            old_name="salary",
            new_name="salarie",
        ),
    ]