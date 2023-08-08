# Generated by Django 4.2.3 on 2023-08-04 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0036_bimaerpunitofmeasure_is_default_for_service_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle",
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
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle_number_to_repeat",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle_stop_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_cycle_stopped_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_initial_parent_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_initial_parent_public_id",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_interval_type_custom_number",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="bimaerpsaledocument",
            name="recurring_interval_type_custom_unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("UNDEFINED", "INDEFINIE"),
                    ("END_AT", "TERMINE LE"),
                    ("END_AFTER", "TERMINE APRES"),
                ],
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle",
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
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle_number_to_repeat",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle_stop_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_cycle_stopped_at",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_initial_parent_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_initial_parent_public_id",
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_interval_type_custom_number",
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name="historicalbimaerpsaledocument",
            name="recurring_interval_type_custom_unit",
            field=models.CharField(
                blank=True,
                choices=[
                    ("UNDEFINED", "INDEFINIE"),
                    ("END_AT", "TERMINE LE"),
                    ("END_AFTER", "TERMINE APRES"),
                ],
                null=True,
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
            ),
        ),
    ]