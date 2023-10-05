from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
import pytz
from common.enums.vacation import VacationStatus
from company.models import BimaCompany
from django.apps import apps
from django.db import models
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django.utils.translation import gettext_lazy as _
from hr.vacation.models import BimaHrVacation
from openpyxl.styles import Border, Side


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
    current_balance = 0
    if hiring_date.year == current_year:
        worked_months = datetime.now().month - hiring_date.month + 1
        current_balance = worked_months * vacation_coefficient
        employee.balance_vacation = current_balance

    elif hiring_date.year < current_year:
        current_balance = datetime.now().month * vacation_coefficient
        employee.balance_vacation = current_balance

    vacation_from_total_working_days_upcoming = sum(
        working_days_count(
            vacation.date_start, vacation.date_end,
            bima_company.start_working_day, bima_company.end_working_day
        )
        for vacation in BimaHrVacation.objects.filter(
            employee=employee,
            date_start__lte=datetime.now(),
            status__in=[VacationStatus.APPROVED.name]
        )
    )
    new_balance_vacation = employee.balance_vacation - vacation_from_total_working_days_upcoming
    employee.balance_vacation = round(new_balance_vacation, 2)

    last_vacation_date = BimaHrVacation.objects.filter(
        employee=employee,
        date_end__lte=end_of_year,
        status__in=[VacationStatus.APPROVED.name]
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
                date_start__lte=last_vacation_date,
                status__in=[VacationStatus.APPROVED.name]
            )
        )
    else:
        expected_new_balance = 0
        total_working_days_upcoming = 0

    new_virtual_balance = current_balance + expected_new_balance - total_working_days_upcoming
    employee.virtual_balance_vacation = round(new_virtual_balance, 2)

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


class BimaHrVacationExportService:

    def __init__(self, queryset):
        self.queryset = queryset
        print(pytz)

    @staticmethod
    def remove_timezone(series):
        return series.dt.tz_localize(None)

    def to_dataframe(self):
        qs_values = self.queryset.annotate(
            employee_full_name=Concat(
                'employee__first_name', Value(' '), 'employee__last_name',
                output_field=CharField()
            ),
            manager_full_name=Concat(
                'manager__first_name', Value(' '), 'manager__last_name',
                output_field=CharField()
            )
        ).values(
            'employee_full_name', 'employee__balance_vacation',
            'manager_full_name', 'date_start', 'date_end',
            'vacation_type', 'status',
            'request_date', 'status_change_date'
        )

        df = pd.DataFrame.from_records(qs_values)

        # Specify column order
        columns_order = [
            'employee_full_name', 'employee__balance_vacation',
            'manager_full_name', 'date_start', 'date_end',
            'vacation_type', 'status',
            'request_date', 'status_change_date'
        ]
        df = df[columns_order]

        datetime_cols = [col for col in df.select_dtypes(include=['datetime64[ns, UTC]']).columns]
        df[datetime_cols] = df[datetime_cols].apply(self.remove_timezone)

        return df

    def translate_enum_values(self, df):
        vacation_type_mapping = {
            'ANNUAL': _('Annual'),
            'SICK': _('Sick'),
            'UNPAID': _('Unpaid'),
            'OTHER': _('Other')
        }
        status_mapping = {
            'PENDING': _('Pending'),
            'APPROVED': _('Approved'),
            'REFUSED': _('Refused')
        }
        df['vacation_type'] = df['vacation_type'].map(vacation_type_mapping)
        df['status'] = df['status'].map(status_mapping)
        return df

    def export_to_csv(self):
        df = self.to_dataframe()
        df = self.translate_enum_values(df)
        df.columns = [
            _('Employee'), _('Vacation Balance'),
            _('Manager'), _('Start Date'), _('End Date'),
            _('Vacation Type'), _('Status'),
            _('Request Date'), _('Date Approve/Refuse')
        ]
        buffer = BytesIO()
        df.to_csv(buffer, index=False)
        return buffer.getvalue()

    def export_to_excel(self):
        df = self.to_dataframe()
        df = self.translate_enum_values(df)
        df.columns = [
            _('Employee'), _('Vacation Balance'),
            _('Manager'), _('Start Date'), _('End Date'),
            _('Vacation Type'), _('Status'),
            _('Request Date'), _('Date Approve/Refuse')
        ]
        buffer = BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)
        return buffer.getvalue()

    def export_employee_vacation_to_excel(self, employee=None):
        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            if employee:
                # Export single employee data
                data = {
                    _('Employee'): [employee.full_name],
                    _('Vacation Balance'): [employee.balance_vacation],
                    _('Vacation Virtual Balance'): [employee.virtual_balance_vacation],
                }
                df = pd.DataFrame(data)
                df.to_excel(writer, index=False, sheet_name='Employee Info')

                vacations = employee.bimahrvacation_set.all().values('date_start', 'date_end', 'status', 'request_date',
                                                                     'status_change_date')
                df_vacations = pd.DataFrame.from_records(vacations)
                df_vacations.columns = [_('start_date'), _('end_date'), _('status'), _('request_date'),
                                        _('date_approve_refuse')]
                df_vacations.to_excel(writer, index=False, sheet_name='Vacations')

            else:
                BimaHrEmployee = apps.get_model('hr', 'BimaHrEmployee')
                employees = BimaHrEmployee.objects.all()
                data = {
                    _('Employee'): [e.full_name for e in employees],
                    _('Vacation Balance'): [e.balance_vacation for e in employees],
                    _('Vacation Virtual Balance'): [e.virtual_balance_vacation for e in employees],
                }
                df = pd.DataFrame(data)
                df.to_excel(writer, index=False, sheet_name='Employees Info')

            workbook = writer.book

            thin_border = Border(left=Side(style='thin'),
                                 right=Side(style='thin'),
                                 top=Side(style='thin'),
                                 bottom=Side(style='thin'))
            for sheet_name in workbook.sheetnames:
                worksheet = workbook[sheet_name]
                for row in worksheet.iter_rows():
                    for cell in row:
                        cell.border = thin_border

        buffer.seek(0)
        return buffer.getvalue()
