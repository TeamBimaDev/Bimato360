# Generated by Django 5.0.6 on 2024-07-03 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0010_alter_bimahrvacancie_job_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bimahroffre",
            name="salary",
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
