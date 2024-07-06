import django_filters

from .models import BimaHrVacation


class BimaHrVacationFilter(django_filters.FilterSet):
    employee = django_filters.UUIDFilter(field_name="employee__public_id")
    manager = django_filters.UUIDFilter(field_name="manager__public_id")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = BimaHrVacation
        fields = ['employee', 'manager', 'status']
