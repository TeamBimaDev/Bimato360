# Generated by Django 5.0.6 on 2024-08-01 19:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0020_alter_bimahrapplicantpost_status_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BimaHrEmployeeinterviewer",
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
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr.bimahremployee",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BimaHrTechnicalInterview",
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
                ("title", models.CharField(max_length=256)),
                ("description", models.TextField(blank=True, null=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "interview_mode",
                    models.CharField(
                        blank=True,
                        choices=[("ONLINE", "Online"), ("PHYSICAL", "Physical")],
                        max_length=64,
                        null=True,
                    ),
                ),
                ("location", models.CharField(blank=True, max_length=256, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("COMPLETED", "Completed"),
                            ("EXPIRED", "Expired"),
                            ("PLANNED", "Planned"),
                            ("CANCELED", "Canceled"),
                        ],
                        max_length=64,
                        null=True,
                    ),
                ),
                ("link_interview", models.URLField(blank=True, null=True)),
                ("record_path", models.URLField(blank=True, max_length=256, null=True)),
                (
                    "candidat",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr.bimahrcandidat",
                    ),
                ),
                (
                    "interview_step",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="hr.bimahrinterviewstep",
                    ),
                ),
                (
                    "interviewer",
                    models.ManyToManyField(
                        through="hr.BimaHrEmployeeinterviewer", to="hr.bimahremployee"
                    ),
                ),
                (
                    "vacancie",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr.bimahrvacancie",
                    ),
                ),
            ],
            options={
                "permissions": [],
            },
        ),
        migrations.AddField(
            model_name="bimahremployeeinterviewer",
            name="technical_interview",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="hr.bimahrtechnicalinterview",
            ),
        ),
    ]