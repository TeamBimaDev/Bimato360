# Generated by Django 4.2.3 on 2023-10-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hr", "0015_bimahrvacation_request_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bimahrvacation",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("APPROVED", "Approved"),
                    ("REFUSED", "Refused"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
    ]