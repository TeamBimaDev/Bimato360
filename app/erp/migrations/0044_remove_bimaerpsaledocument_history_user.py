# Generated by Django 4.2.3 on 2023-08-08 12:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("erp", "0043_remove_historicalbimaerpsaledocument_history_user_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="bimaerpsaledocument",
            name="history_user",
        ),
    ]