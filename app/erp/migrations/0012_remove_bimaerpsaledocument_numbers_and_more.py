# Generated by Django 4.2.1 on 2023-06-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0011_bimaerpsaledocument_bimaerpproduct_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bimaerpsaledocument',
            name='numbers',
        ),
        migrations.RemoveField(
            model_name='historicalbimaerpsaledocument',
            name='numbers',
        ),
        migrations.AddField(
            model_name='bimaerpsaledocument',
            name='number',
            field=models.CharField(default=None, max_length=32, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalbimaerpsaledocument',
            name='number',
            field=models.CharField(db_index=True, default='default', max_length=32),
            preserve_default=False,
        ),
    ]