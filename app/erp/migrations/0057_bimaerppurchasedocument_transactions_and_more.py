# Generated by Django 4.2.3 on 2023-08-31 12:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("treasury", "0022_transactionpurchasedocumentpayment"),
        ("erp", "0056_bimaerppurchasedocument_amount_paid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimaerppurchasedocument",
            name="transactions",
            field=models.ManyToManyField(
                related_name="purchase_documents",
                through="treasury.TransactionPurchaseDocumentPayment",
                to="treasury.bimatreasurytransaction",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimaerppurchasedocument",
            name="amount_paid",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Amount Paid",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimaerppurchasedocument",
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