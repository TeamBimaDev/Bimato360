# Generated by Django 4.2.2 on 2023-07-10 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_password_change_when_created',
            field=models.BooleanField(default=True),
        ),
    ]
