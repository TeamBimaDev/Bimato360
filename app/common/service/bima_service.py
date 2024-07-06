from datetime import timedelta

from company.models import BimaCompany


class BimaService:
    @staticmethod
    def working_days_count(start_date, end_date, start_working_day, end_working_day):
        total_days = 0
        current_day = start_date
        while current_day <= end_date:
            if start_working_day <= current_day.weekday() <= end_working_day:
                total_days += 1
            current_day += timedelta(days=1)
        return total_days

    @staticmethod
    def get_working_days_for_company(company_public_id=None):
        bima_company = BimaCompany.objects.first()  # TODO: Handle case where there are many BimaCompany
        if company_public_id:
            bima_company = BimaCompany.objects.get_object_by_public_id(company_public_id)
        return bima_company.start_working_day, bima_company.end_working_day
