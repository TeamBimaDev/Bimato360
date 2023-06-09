# Generated by Django 4.2.1 on 2023-06-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0004_alter_bimaerppartner_company_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bimaerppartner',
            name='first_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='bimaerppartner',
            name='gender',
            field=models.CharField(blank=True, choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='bimaerppartner',
            name='id_number',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='bimaerppartner',
            name='last_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='bimaerppartner',
            name='social_security_number',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]