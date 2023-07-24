# Generated by Django 4.2.2 on 2023-06-21 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_bimacorecountry_phone_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='bimacorecountry',
            name='capital',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bimacorecountry',
            name='iso2',
            field=models.CharField(blank=True, max_length=256, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='bimacorecountry',
            name='iso3',
            field=models.CharField(blank=True, max_length=256, null=True, unique=True),
        ),
    ]
