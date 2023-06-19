# Generated by Django 4.2.1 on 2023-06-19 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0021_alter_bimaerpproduct_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bimaerpsaledocument',
            name='is_recurring',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='bimaerpsaledocument',
            name='recurring_interval',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'every day'), (30, 'monthly'), (90, 'three monthly'), (365, 'yearly')], help_text='Interval for recurring sale documents', null=True),
        ),
        migrations.AddField(
            model_name='bimaerpsaledocumentproduct',
            name='unit_of_measure',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalbimaerpsaledocument',
            name='is_recurring',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='historicalbimaerpsaledocument',
            name='recurring_interval',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'every day'), (30, 'monthly'), (90, 'three monthly'), (365, 'yearly')], help_text='Interval for recurring sale documents', null=True),
        ),
        migrations.AddField(
            model_name='historicalbimaerpsaledocumentproduct',
            name='unit_of_measure',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]