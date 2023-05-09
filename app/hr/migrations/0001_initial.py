# Generated by Django 4.2.1 on 2023-05-09 12:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BimaHrActivityType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=28)),
                ('description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BimaHrApplicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=28)),
                ('last_name', models.CharField(max_length=28)),
                ('middle_name', models.CharField(max_length=28)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE '), ('OTHER', 'OTHER')], max_length=36)),
                ('social_status', models.CharField(choices=[('SINGLE', 'SINGLE'), ('MARRIED', 'MARRIED'), ('DIVORCED', 'DIVORCED'), ('WIDOWED', 'WIDOWED')], max_length=36)),
                ('kids_number', models.IntegerField()),
                ('social_security_number', models.CharField(max_length=255)),
                ('id_document_number', models.CharField(max_length=255)),
                ('birth_date', models.DateField()),
                ('birth_state', models.CharField(max_length=255)),
                ('birth_country', models.IntegerField()),
                ('priority', models.SmallIntegerField()),
                ('availability_days', models.IntegerField()),
                ('description', models.TextField(max_length=256)),
                ('status', models.SmallIntegerField()),
                ('refuse', models.CharField(max_length=28)),
                ('source_name', models.TextField(max_length=256)),
                ('score', models.FloatField()),
                ('comments', models.TextField(max_length=256)),
                ('id_source_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.bimacoresource')),
            ],
            options={
                'ordering': ['first_name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaHrInterviewStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='SkillLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='hr.skillcategory')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaHrSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('applicant', models.ManyToManyField(blank=True, null=True, related_name='skill_condidat', to='hr.bimahrapplicant')),
                ('skillcategorys', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hr.skillcategory')),
            ],
            options={
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaHrRefuse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('raison', models.CharField(max_length=528)),
                ('date', models.DateTimeField()),
                ('id_manager', models.IntegerField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hr.bimahrapplicant')),
                ('poste', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.bimacoreposte')),
            ],
            options={
                'ordering': ['raison'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaHrInterview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=28)),
                ('date', models.DateTimeField()),
                ('id_interviewer', models.IntegerField()),
                ('note', models.TextField(max_length=255)),
                ('score', models.SmallIntegerField()),
                ('result', models.SmallIntegerField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hr.bimahrapplicant')),
                ('steps', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='hr.bimahrinterviewstep')),
            ],
            options={
                'ordering': ['name'],
                'permissions': [],
            },
        ),
        migrations.CreateModel(
            name='BimaHrCondidatPoste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('expected_salary', models.FloatField(blank=True, default=None, null=True)),
                ('proposed_salary', models.FloatField(blank=True, default=None, null=True)),
                ('accepted_salary', models.FloatField(blank=True, default=None, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('id_candidat', models.ManyToManyField(blank=True, null=True, related_name='condidat_postes', to='hr.bimahrapplicant')),
                ('id_poste', models.ManyToManyField(blank=True, null=True, related_name='condidat_postes', to='core.bimacoreposte')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bimahrapplicant',
            name='steps',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.bimahrinterviewstep'),
        ),
        migrations.CreateModel(
            name='BimaHrActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=28)),
                ('description', models.TextField()),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('id_manager', models.IntegerField()),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.bimahrapplicant')),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hr.bimahractivitytype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
