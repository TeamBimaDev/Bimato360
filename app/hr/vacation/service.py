from datetime import datetime, timedelta

from common.enums.vacation import VacationStatus
from company.models import BimaCompany
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
    current_year = datetime.now().year
    hiring_year = employee.hiring_date.year
    worked_months = (current_year - hiring_year) * 12 if current_year > hiring_year else (
            datetime.now().month - employee.hiring_date.month
    )

    bima_company = BimaCompany.objects.first()  # TODO need to verify the company data
    vacation_coefficient = bima_company.vacation_coefficient

    total_working_days_approved = sum(
        working_days_count(vacation.date_start, vacation.date_end, bima_company.start_working_day,
                           bima_company.end_working_day)
        for vacation in BimaHrVacation.objects.filter(
            employee=employee,
            date_end__gte=datetime.now(),
            status=VacationStatus.APPROVED.value
        )
    )

    total_working_days_upcoming = sum(
        working_days_count(vacation.date_start, vacation.date_end, bima_company.start_working_day,
                           bima_company.end_working_day)
        for vacation in BimaHrVacation.objects.filter(
            employee=employee,
            date_end__gte=datetime.now(),
            status__in=[VacationStatus.APPROVED.value, VacationStatus.PENDING.value]
        )
    )

    balance_vacation = vacation_coefficient * worked_months - total_working_days_approved
    virtual_balance_vacation = balance_vacation - (total_working_days_upcoming - total_working_days_approved)

    employee.balance_vacation = balance_vacation
    employee.virtual_balance_vacation = virtual_balance_vacation
    employee.save()


def is_vacation_request_valid(vacation):
    bima_company = BimaCompany.objects.first()
    requested_working_days = working_days_count(vacation.date_start, vacation.date_end, bima_company.start_working_day,
                                                bima_company.end_working_day)
    return requested_working_days <= vacation.employee.balance_vacation, requested_working_days


def update_vacation_status(vacation, status_update, reason_refused=None):
    if status_update == VacationStatus.APPROVED.value:
        vacation.status = VacationStatus.APPROVED.value
    elif status_update == VacationStatus.REFUSED.value and reason_refused:
        vacation.status = VacationStatus.REFUSED.value
        vacation.reason_refused = reason_refused
    else:
        raise ValueError('Invalid data')
    vacation.save()
    calculate_vacation_balances(vacation.employee)
    return vacation
