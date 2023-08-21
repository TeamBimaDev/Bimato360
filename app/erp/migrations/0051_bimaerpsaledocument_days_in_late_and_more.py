# Generated by Django 4.2.3 on 2023-08-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0050_alter_bimaerpsaledocument_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="days_in_late",
            field=models.PositiveIntegerField(default=0, verbose_name="Days in Late"),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="is_payment_late",
            field=models.BooleanField(default=False, verbose_name="Is Payment Late?"),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="last_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Last Due Date"),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="next_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Next Due Date"),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="days_in_late",
            field=models.PositiveIntegerField(default=0, verbose_name="Days in Late"),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="is_payment_late",
            field=models.BooleanField(default=False, verbose_name="Is Payment Late?"),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="last_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Last Due Date"),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="next_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Next Due Date"),
        ),
    ]
