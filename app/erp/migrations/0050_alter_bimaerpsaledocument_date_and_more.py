# Generated by Django 4.2.3 on 2023-08-18 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("erp", "0049_remove_bimaerppurchasedocument_payment_term_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="date",
            field=models.DateField(verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="delivery_terms",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Delivery Terms"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="is_recurring",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Is Recurring?"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="is_recurring_ended",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Is Recurring Ended?"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="is_recurring_parent",
            field=models.BooleanField(
                blank=True,
                default=False,
                null=True,
                verbose_name="Is Recurring Parent?",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="note",
            field=models.TextField(blank=True, null=True, verbose_name="Note"),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="number",
            field=models.CharField(max_length=32, unique=True, verbose_name="Number"),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="parents",
            field=models.ManyToManyField(
                blank=True, to="erp.bimaerpsaledocument", verbose_name="Parents"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="partner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="erp.bimaerppartner",
                verbose_name="Partner",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="payment_terms",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Payment Terms"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="private_note",
            field=models.TextField(blank=True, null=True, verbose_name="Private Note"),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle",
            field=models.CharField(
                blank=True,
                choices=[
                    ("UNDEFINED", "INDEFINIE"),
                    ("END_AT", "TERMINE LE"),
                    ("END_AFTER", "TERMINE APRES"),
                ],
                null=True,
                verbose_name="Recurring Cycle",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle_number_to_repeat",
            field=models.PositiveIntegerField(
                blank=True,
                default=0,
                null=True,
                verbose_name="Recurring Cycle Number to Repeat",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle_stop_at",
            field=models.DateField(
                blank=True, null=True, verbose_name="Recurring Cycle Stop At"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle_stopped_at",
            field=models.DateField(
                blank=True, null=True, verbose_name="Recurring Cycle Stopped At"
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_initial_parent_id",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Initial Parent ID",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_initial_parent_public_id",
            field=models.UUIDField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Initial Parent Public ID",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_interval",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DAILY", "QUOTIDIEN"),
                    ("WEEKLY", "HEBDOMADAIRE"),
                    ("MONTHLY", "MENSUEL"),
                    ("QUARTERLY", "TRIMESTRIEL"),
                    ("YEARLY", "ANNUEL"),
                    ("CUSTOM", "PERSONNALISE"),
                ],
                help_text="Interval for recurring sale documents",
                null=True,
                verbose_name="Recurring Interval",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_interval_type_custom_number",
            field=models.PositiveIntegerField(
                blank=True,
                default=0,
                null=True,
                verbose_name="Recurring Interval Type Custom Number",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_interval_type_custom_unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DAY", "JOUR"),
                    ("WEEK", "SEMAINE"),
                    ("MONTH", "MOIS"),
                    ("YEAR", "ANNEE"),
                ],
                null=True,
                verbose_name="Recurring Interval Type Custom Unit",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_last_generated_day",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Last Generated Day",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_next_generated_day",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Next Generated Day",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_reactivated_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reactivated_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Recurring Reactivated By",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_reactivated_date",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Reactivated Date",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_reason_reactivated",
            field=models.TextField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Reason Reactivated",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_reason_stop",
            field=models.TextField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Reason Stop",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="recurring_stopped_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stopped_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Recurring Stopped By",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="sale_document_products",
            field=models.ManyToManyField(
                through="erp.BimaErpSaleDocumentProduct",
                to="erp.bimaerpproduct",
                verbose_name="Sale Document Products",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Draft"),
                    ("CONFIRMED", "Confirmed"),
                    ("CANCELED", "CANCELED"),
                ],
                default="DRAFT",
                max_length=128,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="total_after_discount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total After Discount",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="total_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total Amount",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="total_amount_without_vat",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total Amount without VAT",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="total_discount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total Discount",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="total_vat",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total VAT",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="type",
            field=models.CharField(
                choices=[
                    ("QUOTE", "Quote"),
                    ("ORDER", "ORDER"),
                    ("INVOICE", "Invoice"),
                    ("CREDIT_NOTE", "Credit note"),
                ],
                default="Quote",
                max_length=128,
                verbose_name="Type",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="validity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("day_30", "30 days"),
                    ("day_15", "15 days"),
                    ("day_10", "10 days"),
                    ("day_45", "45 days"),
                ],
                null=True,
                verbose_name="Validity",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="vat_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="VAT Amount",
            ),
        ),
        migrations.AlterField(
            model_name="bimaerpsaledocument",
            name="vat_label",
            field=models.CharField(
                blank=True,
                default="",
                max_length=128,
                null=True,
                verbose_name="VAT Label",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="date",
            field=models.DateField(verbose_name="Date"),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="delivery_terms",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Delivery Terms"
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="is_recurring",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Is Recurring?"
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="is_recurring_ended",
            field=models.BooleanField(
                blank=True, default=False, null=True, verbose_name="Is Recurring Ended?"
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="is_recurring_parent",
            field=models.BooleanField(
                blank=True,
                default=False,
                null=True,
                verbose_name="Is Recurring Parent?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="note",
            field=models.TextField(blank=True, null=True, verbose_name="Note"),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="number",
            field=models.CharField(db_index=True, max_length=32, verbose_name="Number"),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
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
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="payment_terms",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Payment Terms"
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="private_note",
            field=models.TextField(blank=True, null=True, verbose_name="Private Note"),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle",
            field=models.CharField(
                blank=True,
                choices=[
                    ("UNDEFINED", "INDEFINIE"),
                    ("END_AT", "TERMINE LE"),
                    ("END_AFTER", "TERMINE APRES"),
                ],
                null=True,
                verbose_name="Recurring Cycle",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle_number_to_repeat",
            field=models.PositiveIntegerField(
                blank=True,
                default=0,
                null=True,
                verbose_name="Recurring Cycle Number to Repeat",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle_stop_at",
            field=models.DateField(
                blank=True, null=True, verbose_name="Recurring Cycle Stop At"
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle_stopped_at",
            field=models.DateField(
                blank=True, null=True, verbose_name="Recurring Cycle Stopped At"
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_initial_parent_id",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Initial Parent ID",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_initial_parent_public_id",
            field=models.UUIDField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Initial Parent Public ID",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_interval",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DAILY", "QUOTIDIEN"),
                    ("WEEKLY", "HEBDOMADAIRE"),
                    ("MONTHLY", "MENSUEL"),
                    ("QUARTERLY", "TRIMESTRIEL"),
                    ("YEARLY", "ANNUEL"),
                    ("CUSTOM", "PERSONNALISE"),
                ],
                help_text="Interval for recurring sale documents",
                null=True,
                verbose_name="Recurring Interval",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_interval_type_custom_number",
            field=models.PositiveIntegerField(
                blank=True,
                default=0,
                null=True,
                verbose_name="Recurring Interval Type Custom Number",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_interval_type_custom_unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DAY", "JOUR"),
                    ("WEEK", "SEMAINE"),
                    ("MONTH", "MOIS"),
                    ("YEAR", "ANNEE"),
                ],
                null=True,
                verbose_name="Recurring Interval Type Custom Unit",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_last_generated_day",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Last Generated Day",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_next_generated_day",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Next Generated Day",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_reactivated_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Recurring Reactivated By",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_reactivated_date",
            field=models.DateField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Reactivated Date",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_reason_reactivated",
            field=models.TextField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Reason Reactivated",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_reason_stop",
            field=models.TextField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Recurring Reason Stop",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_stopped_by",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Recurring Stopped By",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Draft"),
                    ("CONFIRMED", "Confirmed"),
                    ("CANCELED", "CANCELED"),
                ],
                default="DRAFT",
                max_length=128,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="total_after_discount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total After Discount",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="total_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total Amount",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="total_amount_without_vat",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total Amount without VAT",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="total_discount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total Discount",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="total_vat",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="Total VAT",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="type",
            field=models.CharField(
                choices=[
                    ("QUOTE", "Quote"),
                    ("ORDER", "ORDER"),
                    ("INVOICE", "Invoice"),
                    ("CREDIT_NOTE", "Credit note"),
                ],
                default="Quote",
                max_length=128,
                verbose_name="Type",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="validity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("day_30", "30 days"),
                    ("day_15", "15 days"),
                    ("day_10", "10 days"),
                    ("day_45", "45 days"),
                ],
                null=True,
                verbose_name="Validity",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="vat_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=3,
                default=0,
                max_digits=18,
                null=True,
                verbose_name="VAT Amount",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbimaerpsaledocument",
            name="vat_label",
            field=models.CharField(
                blank=True,
                default="",
                max_length=128,
                null=True,
                verbose_name="VAT Label",
            ),
        ),
    ]
