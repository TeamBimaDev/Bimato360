# Generated by Django 4.2.3 on 2023-08-31 12:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0057_bimaerppurchasedocument_transactions_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bimaerppurchasedocument",
            name="payment_terms",
        ),
        migrations.RemoveField(
            model_name="historicalbimaerppurchasedocument",
            name="payment_terms",
        ),
    ]