from datetime import date, datetime

from common.enums.employee_enum import get_marital_status_choices
from common.enums.gender import get_gender_choices
from common.validators.date_format_validator import DateFormatValidator
from core.abstract.models import AbstractModel
from core.country.models import BimaCoreCountry
from django.db import models


class BimaHrPerson(AbstractModel):
    unique_id = models.CharField(max_length=32, unique=True, null=True, blank=True)
    gender = models.CharField(max_length=16, choices=get_gender_choices())
    marital_status = models.CharField(max_length=20, choices=get_marital_status_choices(), null=True, blank=True)
    num_children = models.IntegerField(default=0, null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField(null=True, blank=True, validators=[DateFormatValidator.validate])
    place_of_birth = models.CharField(max_length=64, null=True, blank=True)
    country = models.ForeignKey(BimaCoreCountry, on_delete=models.PROTECT, null=True, blank=True)
    nationality = models.CharField(max_length=64, null=True, blank=True)
    identity_card_number = models.CharField(max_length=32, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    second_phone_number = models.CharField(max_length=16, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    education_level = models.CharField(max_length=128, null=True, blank=True)
    latest_degree = models.CharField(max_length=128, null=True, blank=True)
    latest_degree_date = models.DateField(null=True, blank=True, validators=[DateFormatValidator.validate])
    institute = models.CharField(max_length=128, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        self.clean_dates()
        super().save(*args, **kwargs)

    def clean_dates(self):
        date_fields = ['date_of_birth', 'latest_degree_date']
        for field_name in date_fields:
            date_value = getattr(self, field_name)
            if date_value:
                try:
                    datetime.strptime(str(date_value), '%Y-%m-%d')
                except ValueError:
                    setattr(self, field_name, None)


class BimaHrPersonExperience(AbstractModel):
    person = models.ForeignKey(BimaHrPerson, related_name='experiences', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date_begin = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    is_current_position = models.BooleanField(default=False)

    @property
    def experience_duration(self):
        if self.is_current_position:
            end_date = date.today()
        else:
            end_date = self.date_end

        if not end_date:
            return "End date not specified"

        delta = end_date - self.date_begin
        years = delta.days // 365
        months = (delta.days % 365) // 30

        if years and months:
            return f"{years} year(s) and {months} month(s)"
        elif years:
            return f"{years} year(s)"
        else:
            return f"{months} month(s)"

    def __str__(self):
        return f"{self.person} at {self.company_name} : {self.experience_duration}"
