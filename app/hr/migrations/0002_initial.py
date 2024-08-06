# Generated by Django 4.2.3 on 2024-05-21 10:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("hr", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalbimahremployee",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahremployee",
            name="position",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="hr.bimahrposition",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahremployee",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahrcontract",
            name="department",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="core.bimacoredepartment",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahrcontract",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahrapplicant",
            name="country",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="core.bimacorecountry",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahrapplicant",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahractivity",
            name="activity_type",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="hr.bimahractivitytype",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahractivity",
            name="history_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="bimahrskillcategory",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="hr.bimahrskillcategory",
            ),
        ),
        migrations.AddField(
            model_name="bimahrskill",
            name="persons",
            field=models.ManyToManyField(
                through="hr.BimaHrPersonSkill", to="hr.bimahrperson"
            ),
        ),
        migrations.AddField(
            model_name="bimahrskill",
            name="skill_category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrskillcategory"
            ),
        ),
        migrations.AddField(
            model_name="bimahrposition",
            name="department",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.bimacoredepartment",
            ),
        ),
        migrations.AddField(
            model_name="bimahrposition",
            name="job_category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="hr.bimahrjobcategory"
            ),
        ),
        migrations.AddField(
            model_name="bimahrpersonskill",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrperson"
            ),
        ),
        migrations.AddField(
            model_name="bimahrpersonskill",
            name="skill",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrskill"
            ),
        ),
        migrations.AddField(
            model_name="bimahrpersonexperience",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="experiences",
                to="hr.bimahrperson",
            ),
        ),
        migrations.AddField(
            model_name="bimahrperson",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="core.bimacorecountry",
            ),
        ),
        migrations.AddField(
            model_name="bimahrjobcategory",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="children",
                to="hr.bimahrjobcategory",
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="applicant_post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrapplicantpost"
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="interview_step",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="hr.bimahrinterviewstep"
            ),
        ),
        migrations.AddField(
            model_name="bimahrcontractamendment",
            name="contract",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrcontract"
            ),
        ),
        migrations.AddField(
            model_name="bimahrcontract",
            name="department",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.bimacoredepartment",
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="interview_step",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrinterviewstep"
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="position",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrposition"
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="source_type",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.bimacoresource",
            ),
        ),
        migrations.AddField(
            model_name="bimahractivityparticipant",
            name="activity",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahractivity"
            ),
        ),
        migrations.AddField(
            model_name="bimahractivityparticipant",
            name="person",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrperson"
            ),
        ),
        migrations.AddField(
            model_name="bimahractivity",
            name="activity_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahractivitytype"
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahrcontract",
            name="employee",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahrcontract",
            name="manager_who_stopped",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="historicalbimahractivity",
            name="organizer",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahrvacation",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahremployee"
            ),
        ),
        migrations.AddField(
            model_name="bimahrvacation",
            name="manager",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="managed_vacations",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahrposition",
            name="manager",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="directs",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="interviewer",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="interviews_conducted",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahrinterview",
            name="refused_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="interviews_refused",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahremployee",
            name="position",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hr.bimahrposition",
            ),
        ),
        migrations.AddField(
            model_name="bimahremployee",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="employee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="bimahrcontract",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contracts",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahrcontract",
            name="manager_who_stopped",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stopped_contracts",
                to="hr.bimahremployee",
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicantpost",
            name="applicant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahrapplicant"
            ),
        ),
        migrations.AddField(
            model_name="bimahrapplicant",
            name="applicant_posts",
            field=models.ManyToManyField(
                through="hr.BimaHrApplicantPost", to="hr.bimahrposition"
            ),
        ),
        migrations.AddField(
            model_name="bimahractivity",
            name="organizer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="hr.bimahremployee"
            ),
        ),
    ]