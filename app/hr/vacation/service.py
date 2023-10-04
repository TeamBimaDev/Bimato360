from datetime import datetime, timedelta

from common.enums.vacation import VacationStatus
from company.models import BimaCompany
from django.db import models
from hr.vacation.models import BimaHrVacation


def working_days_count(start_date, end_date, start_working_day, end_working_day):
    total_days = 0
    current_day = start_date
    while current_day <= end_date:
        if start_working_day <= current_day.weekday() <= end_working_day:
            total_days += 1
        current_day += timedelta(days=1)
    return total_days


def calculate_vacation_balances(employee):
    bima_company = BimaCompany.objects.first()  # TODO: Handle case where BimaCompany does not exist
    vacation_coefficient = bima_company.vacation_coefficient
    hiring_date = employee.hiring_date if employee.hiring_date else datetime.now()
    current_year = datetime.now().year
    end_of_year = datetime(current_year, 12, 31)

    if hiring_date.year == current_year:
        worked_months = datetime.now().month - hiring_date.month + 1
        employee.balance_vacation = worked_months * vacation_coefficient
    elif hiring_date.year < current_year:
        employee.balance_vacation = datetime.now().month * vacation_coefficient

    total_working_days_upcoming = sum(
        working_days_count(
            vacation.date_start, vacation.date_end,
            bima_company.start_working_day, bima_company.end_working_day
        )
        for vacation in BimaHrVacation.objects.filter(
            employee=employee,
            date_end__gte=datetime.now(),
            status__in=[VacationStatus.APPROVED.value]
        )
    )
    employee.balance_vacation -= total_working_days_upcoming

    last_vacation_date = BimaHrVacation.objects.filter(
        employee=employee,
        date_end__lte=end_of_year,
        status__in=[VacationStatus.APPROVED.value]
    ).aggregate(models.Max('date_end'))['date_end__max']

    if last_vacation_date:
        months_until_last_vacation = last_vacation_date.month - datetime.now().month
        expected_new_balance = months_until_last_vacation * vacation_coefficient

        total_working_days_upcoming = sum(
            working_days_count(
                vacation.date_start, vacation.date_end,
                bima_company.start_working_day, bima_company.end_working_day
            )
            for vacation in BimaHrVacation.objects.filter(
                employee=employee,
                date_end__lte=last_vacation_date,
                status__in=[VacationStatus.APPROVED.value]
            )
        )
    else:
        expected_new_balance = 0
        total_working_days_upcoming = 0

    employee.virtual_balance_vacation = (
            employee.balance_vacation + expected_new_balance - total_working_days_upcoming
    )

    employee.save()


def is_vacation_request_valid(vacation):
    bima_company = BimaCompany.objects.first()
    requested_working_days = working_days_count(vacation.date_start, vacation.date_end, bima_company.start_working_day,
                                                bima_company.end_working_day)
    return requested_working_days <= vacation.employee.balance_vacation, requested_working_days


def update_vacation_status(vacation, status_update, reason_refused=None, save=True):
    if status_update == VacationStatus.APPROVED.value:
        vacation.status = VacationStatus.APPROVED.value
    elif status_update == VacationStatus.REFUSED.value and reason_refused:
        vacation.status = VacationStatus.REFUSED.value
        vacation.reason_refused = reason_refused
    else:
        raise ValueError('Invalid data')
    if save:
        vacation.save()
    calculate_vacation_balances(vacation.employee)
    return vacation
