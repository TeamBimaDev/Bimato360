# Generated by Django 4.2.3 on 2023-08-21 09:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("treasury", "0015_alter_bimatreasurytransactiontype_cash_bank"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bimatreasurypaymenttermdetail",
            name="value",
            field=models.CharField(
                choices=[
                    ("IMMEDIATE", "IMMEDIATE"),
                    ("AFTER_ONE_WEEK", "AFTER_ONE_WEEK"),
                    ("AFTER_TWO_WEEK", "AFTER_TWO_WEEK"),
                    ("END_OF_MONTH", "END_OF_MONTH"),
                    ("NEXT_MONTH", "NEXT_MONTH"),
                ],
                max_length=64,
            ),
        ),
    ]