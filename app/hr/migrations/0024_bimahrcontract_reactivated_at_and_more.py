# Generated by Django 4.2.3 on 2023-10-12 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hr", "0023_alter_bimahrvacation_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimahrcontract",
            name="reactivated_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimahrcontract",
            name="reactivated_at",
            field=models.DateField(blank=True, null=True),
        ),
    ]
