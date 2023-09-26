# Generated by Django 4.2.3 on 2023-09-26 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_bimacoresource_active"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("hr", "0006_bimahrapplicant_bimahrapplicantpost_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalBimaHrEmployee",
            fields=[
                (
                    "bimahrperson_ptr",
                    models.ForeignKey(
                        auto_created=True,
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        related_name="+",
                        to="hr.bimahrperson",
                    ),
                ),
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                (
                    "unique_id",
                    models.CharField(
                        blank=True, db_index=True, max_length=32, null=True
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("MALE", "Male"), ("FEMALE", "Female")], max_length=16
                    ),
                ),
                (
                    "marital_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("SINGLE", "Single"),
                            ("MARRIED", "Married"),
                            ("DIVORCED", "Divorced"),
                            ("WIDOWED", "Widowed"),
                            ("SEPARATED", "Separated"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("num_children", models.IntegerField(blank=True, default=0, null=True)),
                ("first_name", models.CharField(max_length=64)),
                ("last_name", models.CharField(max_length=64)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "place_of_birth",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("nationality", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "identity_card_number",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                (
                    "second_phone_number",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "education_level",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "latest_degree",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("latest_degree_date", models.DateField(blank=True, null=True)),
                ("institute", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "employment_type",
                    models.CharField(
                        choices=[
                            ("PERMANENT", "Permanent"),
                            ("TEMPORARY", "Temporary"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "work_mode",
                    models.CharField(
                        choices=[
                            ("ONSITE", "Onsite"),
                            ("REMOTE", "Remote"),
                            ("HYBRID", "Hybrid"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "job_type",
                    models.CharField(
                        choices=[
                            ("FULL_TIME", "Full-time"),
                            ("PART_TIME", "Part-time"),
                            ("INTERN", "Intern"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "employment_status",
                    models.CharField(
                        choices=[("ACTIVE", "Active"), ("TERMINATED", "Terminated")],
                        max_length=20,
                    ),
                ),
                ("probation_end_date", models.DateField(blank=True, null=True)),
                ("last_performance_review", models.DateField(blank=True, null=True)),
                (
                    "salary",
                    models.DecimalField(
                        blank=True, decimal_places=3, max_digits=10, null=True
                    ),
                ),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="core.bimacorecountry",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "position",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="hr.bimahrposition",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical bima hr employee",
                "verbose_name_plural": "historical bima hr employees",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalBimaHrApplicant",
            fields=[
                (
                    "bimahrperson_ptr",
                    models.ForeignKey(
                        auto_created=True,
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        parent_link=True,
                        related_name="+",
                        to="hr.bimahrperson",
                    ),
                ),
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "public_id",
                    models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
                ),
                ("created", models.DateTimeField(blank=True, editable=False)),
                ("updated", models.DateTimeField(blank=True, editable=False)),
                (
                    "unique_id",
                    models.CharField(
                        blank=True, db_index=True, max_length=32, null=True
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("MALE", "Male"), ("FEMALE", "Female")], max_length=16
                    ),
                ),
                (
                    "marital_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("SINGLE", "Single"),
                            ("MARRIED", "Married"),
                            ("DIVORCED", "Divorced"),
                            ("WIDOWED", "Widowed"),
                            ("SEPARATED", "Separated"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("num_children", models.IntegerField(blank=True, default=0, null=True)),
                ("first_name", models.CharField(max_length=64)),
                ("last_name", models.CharField(max_length=64)),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "place_of_birth",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("nationality", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "identity_card_number",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                (
                    "second_phone_number",
                    models.CharField(blank=True, max_length=16, null=True),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "education_level",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "latest_degree",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("latest_degree_date", models.DateField(blank=True, null=True)),
                ("institute", models.CharField(blank=True, max_length=128, null=True)),
                ("priority", models.SmallIntegerField()),
                ("availability_days", models.IntegerField()),
                ("description", models.TextField(max_length=256)),
                ("comments", models.TextField(max_length=256)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="core.bimacorecountry",
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical bima hr applicant",
                "verbose_name_plural": "historical bima hr applicants",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
