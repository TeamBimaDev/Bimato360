# Generated by Django 5.0.6 on 2024-07-11 16:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0015_remove_bimahrinterview_additional_comments_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bimahrinterview",
            options={"ordering": ["-name"], "permissions": []},
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="date",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="note",
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="candidat",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="hr.bimahrcandidat",
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="due_date",
            field=models.CharField(
                blank=True,
                choices=[
                    ("One_Day", "1 Day"),
                    ("Two_Day", "2 Day"),
                    ("Three_Day", "3 Day"),
                ],
                max_length=64,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="estimated_time",
            field=models.CharField(
                blank=True,
                choices=[
                    ("One_Day", "1 Day"),
                    ("Two_Day", "2 Day"),
                    ("Three_Day", "3 Day"),
                ],
                max_length=64,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="interview_step",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="hr.bimahrinterviewstep",
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="link_interview",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="name",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="scheduled_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="score",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("COMPLETED", "Completed"),
                    ("EXPIRED", "Expired"),
                    ("PLANNED", "Planned"),
                ],
                max_length=64,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="vacancie",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="hr.bimahrvacancie",
            ),
        ),
        migrations.AlterField(
            model_name="bimahrapplicantpost",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[
                    ("COMPLETED", "Completed"),
                    ("EXPIRED", "Expired"),
                    ("PLANNED", "Planned"),
                ],
                max_length=64,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="bimahrinterviewstep",
            name="interview_type",
            field=models.CharField(
                blank=True,
                choices=[("TECHNICAL", "Technical"), ("HR", "Hr")],
                max_length=100,
                null=True,
            ),
        ),
    ]