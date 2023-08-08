# Generated by Django 4.2.3 on 2023-08-07 09:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0039_bimaerpsaledocument_is_recurring_ended_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_last_generated_day",
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_last_generated_day",
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]