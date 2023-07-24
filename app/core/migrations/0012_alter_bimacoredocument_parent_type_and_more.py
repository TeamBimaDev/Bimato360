# Generated by Django 4.2.1 on 2023-06-05 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0011_alter_bimacoredocument_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bimacoredocument',
            name='parent_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='bimacoreentitytag',
            name='parent_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
    ]
