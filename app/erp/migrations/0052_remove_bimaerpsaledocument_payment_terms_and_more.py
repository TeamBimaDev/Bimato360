# Generated by Django 4.2.3 on 2023-08-28 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0051_bimaerpsaledocument_days_in_late_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bimaerpsaledocument",
            name="payment_terms",
        ),
        migrations.RemoveField(
            model_name="historicalbimaerpsaledocument",
            name="payment_terms",
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="payment_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NOT_PAID", "NOT_PAD"),
                    ("PARTIAL_PAID", "PARTIAL_PAID"),
                    ("PAID", "PAID"),
                ],
                default="NOT_PAID",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="payment_status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("NOT_PAID", "NOT_PAD"),
                    ("PARTIAL_PAID", "PARTIAL_PAID"),
                    ("PAID", "PAID"),
                ],
                default="NOT_PAID",
                null=True,
            ),
        ),
    ]