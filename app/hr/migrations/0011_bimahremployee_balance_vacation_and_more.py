# Generated by Django 4.2.3 on 2023-09-29 10:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("hr", "0010_bimahremployee_hiring_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimahremployee",
            name="balance_vacation",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="bimahremployee",
            name="virtual_balance_vacation",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="historicalbimahremployee",
            name="balance_vacation",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="historicalbimahremployee",
            name="virtual_balance_vacation",
            field=models.FloatField(default=0),
        ),
        migrations.CreateModel(
            name="BimaHrVacation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(
                        db_index=True, default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("date_start", models.DateField()),
                ("date_end", models.DateField()),
                ("reason", models.TextField(blank=True, null=True)),
                (
                    "vacation_type",
                    models.CharField(
                        choices=[
                            ("Annual", "Annual"),
                            ("Sick", "Sick"),
                            ("Unpaid", "Unpaid"),
                            ("Other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Approved", "Approved"),
                            ("Refused", "Refused"),
                        ],
                        default="Pending",
                        max_length=20,
                    ),
                ),
                ("reason_refused", models.TextField(blank=True, null=True)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr.bimahremployee",
                    ),
                ),
                (
                    "manager",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="managed_vacations",
                        to="hr.bimahremployee",
                    ),
                ),
            ],
            options={
                "permissions": [],
            },
        ),
    ]
