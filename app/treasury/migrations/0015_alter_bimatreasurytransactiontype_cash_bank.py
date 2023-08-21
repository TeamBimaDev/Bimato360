# Generated by Django 4.2.3 on 2023-08-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("treasury", "0014_alter_bimatreasurypaymenttermdetail_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bimatreasurytransactiontype",
            name="cash_bank",
            field=models.CharField(
                choices=[("CASH", "Cash"), ("BANK", "Bank")],
                max_length=32,
                verbose_name="CASH_BANK",
            ),
        ),
    ]