# Generated by Django 5.0.6 on 2024-08-01 22:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("hr", "0022_remove_bimahrtechnicalinterview_end_date_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="bimahrtechnicalinterview",
            old_name="interviewer",
            new_name="interviewers",
        ),
    ]