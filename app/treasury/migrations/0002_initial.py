# Generated by Django 5.0.6 on 2024-05-21 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("erp", "0003_initial"),
        ("treasury", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalbimatreasurytransaction",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimatreasurytransaction",
            name="partner",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="erp.bimaerppartner",
                verbose_name="Partner",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimatreasurytransaction",
            name="payment_method",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="treasury.bimatreasurypaymentmethod",
                verbose_name="Transaction Type",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimatreasurytransaction",
            name="transaction_source",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="treasury.bimatreasurytransaction",
                verbose_name="Transaction Source",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimatreasurytransaction",
            name="transaction_type",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="treasury.bimatreasurytransactiontype",
                verbose_name="Transaction Type",
            ),
        ),
        migrations.AddField(
            model_name="transactionpurchasedocumentpayment",
            name="purchase_document",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="erp.bimaerppurchasedocument",
            ),
        ),
        migrations.AddField(
            model_name="transactionpurchasedocumentpayment",
            name="transaction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="treasury.bimatreasurytransaction",
            ),
        ),
        migrations.AddField(
            model_name="transactionsaledocumentpayment",
            name="sale_document",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="erp.bimaerpsaledocument",
            ),
        ),
        migrations.AddField(
            model_name="transactionsaledocumentpayment",
            name="transaction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="treasury.bimatreasurytransaction",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="transactionpurchasedocumentpayment",
            unique_together={("transaction", "purchase_document")},
        ),
        migrations.AlterUniqueTogether(
            name="transactionsaledocumentpayment",
            unique_together={("transaction", "sale_document")},
        ),
    ]