# Generated by Django 4.2.1 on 2023-06-16 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_bimacoreentitytag_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bimacorecountry',
            name='phone_code',
            field=models.CharField(blank=True, null=True),
        ),
    ]
