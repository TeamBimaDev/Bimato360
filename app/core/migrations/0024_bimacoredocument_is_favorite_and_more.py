# Generated by Django 4.2.2 on 2023-07-05 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_bimacorecash_alter_bimacorecountry_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bimacoredocument',
            name='is_favorite',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='bimacoredocument',
            name='file_type',
            field=models.CharField(choices=[('PARTNER_PICTURE', 'PARTNER_PICTURE'), ('PARTNER_PRIVATE_DOCUMENT', 'PARTNER_PRIVATE_DOCUMENT'), ('PARTNER_CIRET_DOCUMENT', 'PARTNER_CIRET_DOCUMENT'), ('COMPANY_LOGO', 'Logo'), ('COMPANY_DOCUMENT', 'Documents'), ('EMPLOYEE_CV', 'EMPLOYEE_CV'), ('EMPLOYEE_RESUME', 'EMPLOYEE_RESUME'), ('EMPLOYEE_DRIVER_LICENCE', 'EMPLOYEE_DRIVER_LICENCE'), ('EMPLOYEE_PICTURE', 'EMPLOYEE_PICTURE')], max_length=128),
        ),
    ]
