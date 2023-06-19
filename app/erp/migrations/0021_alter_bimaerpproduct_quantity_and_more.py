# Generated by Django 4.2.1 on 2023-06-16 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0020_bimaerpsaledocument_vat_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bimaerpproduct',
            name='quantity',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bimaerpproduct',
            name='virtual_quantity',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='bimaerpsaledocument',
            name='type',
            field=models.CharField(choices=[('QUOTE', 'Quote'), ('ORDER', 'ORDER'), ('INVOICE', 'Invoice'), ('CREDIT_NOTE', 'Credit note')], default='Quote', max_length=128),
        ),
        migrations.AlterField(
            model_name='historicalbimaerpsaledocument',
            name='type',
            field=models.CharField(choices=[('QUOTE', 'Quote'), ('ORDER', 'ORDER'), ('INVOICE', 'Invoice'), ('CREDIT_NOTE', 'Credit note')], default='Quote', max_length=128),
        ),
    ]