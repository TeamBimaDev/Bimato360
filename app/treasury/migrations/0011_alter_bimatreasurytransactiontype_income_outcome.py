# Generated by Django 4.2.3 on 2023-08-17 11:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("treasury", "0010_bimatreasurytransactiontype_income_outcome"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bimatreasurytransactiontype",
            name="income_outcome",
            field=models.CharField(
                choices=[("INCOME", "INCOME"), ("OUTCOME", "OUTCOME")],
                default=None,
                max_length=32,
                verbose_name="INCOME_OUTCOME",
            ),
            preserve_default=False,
        ),
    ]
