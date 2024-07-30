# Generated by Django 5.0.6 on 2024-07-03 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0012_rename_salary_bimahroffre_salarie"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bimahroffre",
            name="salarie",
        ),
        migrations.AddField(
            model_name="bimahroffre",
            name="salary",
            field=models.DecimalField(
                blank=True, decimal_places=3, max_digits=10, null=True
            ),
        ),
    ]