# Generated by Django 5.0.6 on 2024-07-09 19:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0014_bimahrinterviewquestion"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="additional_comments",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="applicant_post",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="comments",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="interview_step",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="interviewer",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="refusal_date",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="refusal_reason",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="refused_by",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="score",
        ),
        migrations.RemoveField(
            model_name="bimahrinterview",
            name="status",
        ),
    ]