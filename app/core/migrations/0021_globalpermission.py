# Generated by Django 4.2.2 on 2023-06-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_bimacorecontact_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
