# Generated by Django 4.2.3 on 2023-09-19 14:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0062_alter_bimaerppurchasedocument_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="last_generated_file_url",
            field=models.TextField(blank=True, null=True, verbose_name="Fichier"),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="last_generated_file_url",
            field=models.TextField(blank=True, null=True, verbose_name="Fichier"),
        ),
    ]
