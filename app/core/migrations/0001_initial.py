# Generated by Django 4.2.1 on 2023-05-18 08:40

import core.document.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BimaCoreBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('active', models.BooleanField(default=True)),
                ('bic', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('code', models.CharField(blank=True, max_length=256, null=True)),
                ('address_format', models.CharField(blank=True, max_length=256, null=True)),
                ('address_view_id', models.PositiveIntegerField(blank=True, null=True)),
                ('phone_code', models.PositiveIntegerField(null=True)),
                ('name_position', models.CharField(blank=True, max_length=64, null=True)),
                ('vat_label', models.CharField(blank=True, max_length=64, null=True)),
                ('state_required', models.BooleanField(null=True)),
                ('zip_required', models.BooleanField(null=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('symbol', models.CharField(blank=True, max_length=16, null=True)),
                ('rounding', models.PositiveIntegerField(blank=True, null=True)),
                ('decimal_places', models.PositiveIntegerField(blank=True, null=True)),
                ('active', models.BooleanField(null=True)),
                ('position', models.CharField(blank=True, max_length=64, null=True)),
                ('currency_unit_label', models.CharField(blank=True, max_length=64, null=True)),
                ('currency_subunit_label', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('manager_id', models.PositiveIntegerField(blank=True, null=True)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.bimacoredepartment')),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('id_manager', models.IntegerField()),
                ('parent_id', models.PositiveIntegerField()),
                ('parent_type', models.ForeignKey(limit_choices_to={'app_label__in': ['messages', 'staticfiles', 'corsheaders', 'rest_framework', 'drf_spectacular', 'core', 'user', 'hr', 'company', 'partners']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('code', models.CharField(blank=True, max_length=256, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.bimacorecountry')),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCorePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('requirements', models.TextField(blank=True, null=True)),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('department_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bimacoredepartment')),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('parent_id', models.PositiveIntegerField()),
                ('document_name', models.CharField(max_length=30)),
                ('description', models.TextField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('file_extension', models.CharField(max_length=255)),
                ('date_file', models.DateTimeField(auto_now_add=True)),
                ('file_path', models.FileField(upload_to=core.document.models.BimaCoreDocument.document_file_path)),
                ('file_type', models.CharField(choices=[('CV', 'CV'), ('RESUME', 'RESUME'), ('DRIVER_LICENCE', 'DRIVER_LICENCE'), ('PICTURE', 'PICTURE')], max_length=100)),
                ('parent_type', models.ForeignKey(limit_choices_to={'app_label__in': ['messages', 'staticfiles', 'corsheaders', 'rest_framework', 'drf_spectacular', 'core', 'user', 'hr', 'company', 'partners']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['file_name'],
                'permissions': [],
            },
        ),
        migrations.AddField(
            model_name='bimacorecountry',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.bimacorecurrency'),
        ),
        migrations.CreateModel(
            name='BimaCoreContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('fax', models.CharField(max_length=128, unique=True)),
                ('mobile', models.CharField(max_length=128, unique=True)),
                ('phone', models.CharField(max_length=128, unique=True)),
                ('parent_id', models.PositiveIntegerField()),
                ('parent_type', models.ForeignKey(limit_choices_to={'app_label__in': ['messages', 'staticfiles', 'corsheaders', 'rest_framework', 'drf_spectacular', 'core', 'user', 'hr', 'company', 'partners']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['mobile'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaCoreAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(max_length=28)),
                ('street', models.CharField(max_length=256)),
                ('street2', models.CharField(blank=True, max_length=256, null=True)),
                ('zip', models.CharField(max_length=28)),
                ('city', models.CharField(max_length=128)),
                ('parent_id', models.PositiveIntegerField()),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.bimacorecountry')),
                ('parent_type', models.ForeignKey(limit_choices_to={'app_label__in': ['messages', 'staticfiles', 'corsheaders', 'rest_framework', 'drf_spectacular', 'core', 'user', 'hr', 'company', 'partners']}, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.bimacorestate')),
            ],
            options={
                'ordering': ['number'],
                'permissions': [],
            },
        ),
    ]
