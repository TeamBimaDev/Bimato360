# Generated by Django 4.2.3 on 2023-09-26 09:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0036_bimacoresource_active"),
        ("hr", "0005_rename_skill_categories_bimahrskill_skill_category_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BimaHrApplicant",
            fields=[
                (
                    "bimahrperson_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="hr.bimahrperson",
                    ),
                ),
                ("priority", models.SmallIntegerField()),
                ("availability_days", models.IntegerField()),
                ("description", models.TextField(max_length=256)),
                ("comments", models.TextField(max_length=256)),
            ],
            options={
                "ordering": ["first_name"],
                "permissions": [],
            },
            bases=("hr.bimahrperson",),
        ),
        migrations.CreateModel(
            name="BimaHrApplicantPost",
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
                    "expected_salary",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "proposed_salary",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "accepted_salary",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("comments", models.TextField(max_length=256)),
                (
                    "source_name",
                    models.TextField(
                        blank=True, default=None, max_length=256, null=True
                    ),
                ),
                ("score", models.FloatField(blank=True, default=None, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PASSED", "Passed"),
                            ("FAILED", "Failed"),
                            ("REFUSED", "Refused"),
                            ("PENDING", "Pending"),
                            ("IN_PROGRESS", "In Progress"),
                        ],
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "applicant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr.bimahrapplicant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="BimaHrInterviewStep",
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
                ("name", models.CharField(max_length=255)),
                (
                    "interview_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("TECHNICAL", "Technical"),
                            ("HR", "Hr"),
                            ("INITIAL", "Initial"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["name"],
                "permissions": [],
            },
        ),
        migrations.CreateModel(
            name="BimaHrInterview",
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
                ("date", models.DateField()),
                ("note", models.TextField(max_length=255)),
                ("score", models.FloatField(blank=True, null=True)),
                ("comments", models.TextField(blank=True, max_length=256, null=True)),
                (
                    "status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("PASSED", "Passed"),
                            ("FAILED", "Failed"),
                            ("REFUSED", "Refused"),
                            ("PENDING", "Pending"),
                            ("IN_PROGRESS", "In Progress"),
                        ],
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "refusal_reason",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("refusal_date", models.DateField(blank=True, null=True)),
                ("additional_comments", models.TextField(blank=True, null=True)),
                (
                    "applicant_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="hr.bimahrapplicantpost",
                    ),
                ),
                (
                    "interview_step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="hr.bimahrinterviewstep",
                    ),
                ),
                (
                    "interviewer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="interviews_conducted",
                        to="hr.bimahremployee",
                    ),
                ),
                (
                    "refused_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="interviews_refused",
                        to="hr.bimahremployee",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
                "permissions": [],
            },
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="interview_step",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrinterviewstep"
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="position",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrposition"
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="source_type",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.bimacoresource",
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicant",
            name="applicant_posts",
            field=models.ManyToManyField(
                through="hr.BimaHrApplicantPost", to="hr.bimahrposition"
            ),
        ),
    ]
