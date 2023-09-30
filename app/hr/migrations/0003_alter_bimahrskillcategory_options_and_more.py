# Generated by Django 4.2.3 on 2023-09-25 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("hr", "0002_bimahrjobcategory_bimahrperson_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bimahrskillcategory",
            options={"ordering": ["name"], "permissions": []},
        ),
        migrations.RemoveField(
            model_name="bimahremployee",
            name="marital_status",
        ),
        migrations.RemoveField(
            model_name="bimahremployee",
            name="num_children",
        ),
        migrations.AddField(
            model_name="bimahrperson",
            name="marital_status",
            field=models.CharField(
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
        migrations.AddField(
            model_name="bimahrperson",
            name="num_children",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]