# Generated by Django 4.2.1 on 2023-06-02 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0005_alter_bimaerppartner_first_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bimaerppartner',
            old_name='Email',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='bimaerppartner',
            old_name='Fax',
            new_name='fax',
        ),
        migrations.RenameField(
            model_name='bimaerppartner',
            old_name='Phone',
            new_name='phone',
        ),
    ]
