# Generated by Django 4.2.3 on 2023-09-08 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0060_alter_bimaerppurchasedocument_payment_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimaerppurchasedocument",
            name="days_in_late",
            field=models.PositiveIntegerField(default=0, verbose_name="Days in Late"),
        ),
        migrations.AddField(
            model_name="bimaerppurchasedocument",
            name="is_payment_late",
            field=models.BooleanField(default=False, verbose_name="Is Payment Late?"),
        ),
        migrations.AddField(
            model_name="bimaerppurchasedocument",
            name="last_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Last Due Date"),
        ),
        migrations.AddField(
            model_name="bimaerppurchasedocument",
            name="next_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Next Due Date"),
        ),
        migrations.AddField(
            model_name="historicalbimaerppurchasedocument",
            name="days_in_late",
            field=models.PositiveIntegerField(default=0, verbose_name="Days in Late"),
        ),
        migrations.AddField(
            model_name="historicalbimaerppurchasedocument",
            name="is_payment_late",
            field=models.BooleanField(default=False, verbose_name="Is Payment Late?"),
        ),
        migrations.AddField(
            model_name="historicalbimaerppurchasedocument",
            name="last_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Last Due Date"),
        ),
        migrations.AddField(
            model_name="historicalbimaerppurchasedocument",
            name="next_due_date",
            field=models.DateField(blank=True, null=True, verbose_name="Next Due Date"),
        ),
    ]
