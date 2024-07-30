# Generated by Django 5.0.6 on 2024-05-21 14:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("company", "0002_initial"),
        ("core", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="bimacorenotification",
            name="sender",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="sent_notifications",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="bimacorenotificationtemplate",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="company.bimacompany"
            ),
        ),
        migrations.AddField(
            model_name="bimacorenotificationtemplate",
            name="notification_type",
            field=models.OneToOneField(
                error_messages={
                    "unique": "A template with this notification type already exists."
                },
                on_delete=django.db.models.deletion.CASCADE,
                to="core.bimacorenotificationtype",
            ),
        ),
        migrations.AddField(
            model_name="bimacorenotification",
            name="notification_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.bimacorenotificationtype",
            ),
        ),
        migrations.AddField(
            model_name="bimacorestate",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="core.bimacorecountry"
            ),
        ),
        migrations.AddField(
            model_name="bimacoreaddress",
            name="state",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="core.bimacorestate"
            ),
        ),
        migrations.AddField(
            model_name="bimacoretag",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="core.bimacoretag",
            ),
        ),
        migrations.AddField(
            model_name="bimacoreentitytag",
            name="tag",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="core.bimacoretag"
            ),
        ),
    ]