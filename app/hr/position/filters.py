<<<<<<< HEAD
import django_filters
from common.enums.position import get_seniority_choices
from django.db import models
from django_filters import rest_framework as filters

from .models import BimaHrPosition


class BimaHrPositionFilter(filters.FilterSet):
    department = django_filters.UUIDFilter(field_name='department__public_id')
    job_category = django_filters.UUIDFilter(field_name='job_category__public_id')
    manager = django_filters.UUIDFilter(field_name='manager__public_id')
    seniority = django_filters.ChoiceFilter(choices=get_seniority_choices())

    search = django_filters.CharFilter(
        method='filter_search',
        label='Search in title, description, requirements, and responsibilities',
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(requirements__icontains=value) |
            models.Q(responsibilities__icontains=value)
        )

    class Meta:
        model = BimaHrPosition
        fields = []
=======
import django_filters
from common.enums.position import get_seniority_choices
from django.db import models
from django_filters import rest_framework as filters

from .models import BimaHrPosition


class BimaHrPositionFilter(filters.FilterSet):
    department = django_filters.UUIDFilter(field_name='department__public_id')
    job_category = django_filters.UUIDFilter(field_name='job_category__public_id')
    manager = django_filters.UUIDFilter(field_name='manager__public_id')
    seniority = django_filters.ChoiceFilter(choices=get_seniority_choices())

    search = django_filters.CharFilter(
        method='filter_search',
        label='Search in title, description, requirements, and responsibilities',
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(requirements__icontains=value) |
            models.Q(responsibilities__icontains=value)
        )

    class Meta:
        model = BimaHrPosition
        fields = []
>>>>>>> origin/ma-branch
