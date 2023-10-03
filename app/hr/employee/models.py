from common.enums.employee_enum import get_employment_type_choices, \
    get_work_mode_choices, get_job_type_choices, get_employee_status_choices
from common.exceptions.email_required_validation import EmailRequiredValidation
from common.exceptions.user_exists_validation import UserExistsValidation
from django.contrib.auth import get_user_model
from django.db import models
from hr.models import BimaHrPerson
from hr.position.models import BimaHrPosition
from simple_history.models import HistoricalRecords


class BimaHrEmployee(BimaHrPerson):
    employment_type = models.CharField(max_length=20, choices=get_employment_type_choices(), null=True, blank=True)
    work_mode = models.CharField(max_length=20, choices=get_work_mode_choices(), null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=get_job_type_choices(), null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=get_employee_status_choices(), null=True, blank=True)
    hiring_date = models.DateField(null=True, blank=True)
    probation_end_date = models.DateField(null=True, blank=True)
    last_performance_review = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    position = models.ForeignKey(BimaHrPosition, blank=True, null=True, on_delete=models.SET_NULL)
    balance_vacation = models.FloatField(default=0)
    virtual_balance_vacation = models.FloatField(default=0)
    user = models.OneToOneField(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='employee')
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name, self.last_name}"

    class Meta:
        ordering = ['first_name']
        permissions = []
        default_permissions = ()

    @property
    def is_user_account_created(self):
        return self.user is not None

    def create_user_account(self, password, **extra_fields):
        if self.user:
            return self.user

        if not self.email:
            raise EmailRequiredValidation()

        if get_user_model().objects.filter(email=self.email).exists():
            raise UserExistsValidation()

        random_password = get_user_model().objects.make_random_password()
        user = get_user_model().objects.create_user(
            email=self.email,
            password=random_password,
            name=self.full_name,
            is_password_change_when_created=True,
            created_by_admin=True,
            **extra_fields
        )
        self.user = user
        self.save()

        return user
