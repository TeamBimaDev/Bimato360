# Generated by Django 5.0.6 on 2024-06-25 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0004_alter_bimahrvacancie_position_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="bimahrcandidatvacancie",
            name="score",
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]