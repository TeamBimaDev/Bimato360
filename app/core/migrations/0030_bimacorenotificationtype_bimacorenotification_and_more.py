# Generated by Django 4.2.3 on 2023-09-15 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("company", "0010_alter_bimacompany_default_font_family"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0029_delete_bimacorecash"),
    ]

    operations = [
        migrations.CreateModel(
            name="BimaCoreNotificationType",
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
                ("name", models.CharField(max_length=128)),
                ("active", models.BooleanField(default=True)),
                (
                    "code",
                    models.CharField(
                        blank=True, max_length=128, null=True, unique=True
                    ),
                ),
                ("is_system", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["name"],
                "permissions": [],
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="BimaCoreNotification",
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
                ("receivers_email", models.JSONField(blank=True, null=True)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("attachments", models.JSONField(blank=True, null=True)),
                ("date_sent", models.DateTimeField(auto_now_add=True)),
                ("parent_id", models.PositiveIntegerField()),
                (
                    "notification_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.bimacorenotificationtype",
                    ),
                ),
                (
                    "parent_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sent_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["date_sent"],
                "permissions": [],
                "default_permissions": (),
            },
        ),
        migrations.CreateModel(
            name="BimaCoreNotificationTemplate",
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
                ("name", models.CharField(max_length=128)),
                ("subject", models.CharField(max_length=255)),
                ("message", models.TextField(blank=True, null=True)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="company.bimacompany",
                    ),
                ),
                (
                    "notification_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.bimacorenotificationtype",
                    ),
                ),
            ],
            options={
                "ordering": ["name"],
                "permissions": [],
                "default_permissions": (),
                "unique_together": {("notification_type",)},
            },
        ),
    ]
