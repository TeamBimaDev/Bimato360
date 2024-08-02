import django_filters
from common.enums.interview import get_interview_status_choices, get_interview_mode_choices
from django.db import models
from django_filters import rest_framework as filters

from .models import BimaHrTechnicalInterview


class BimaHrTechnicalInterviewFilter(filters.FilterSet):

    vacancie = django_filters.UUIDFilter(field_name='vacancie__public_id')
    candidat = django_filters.UUIDFilter(field_name='candidat__public_id')
    interview_step = django_filters.UUIDFilter(field_name='interview_step__public_id')
    interview_mode = django_filters.ChoiceFilter(choices=get_interview_mode_choices())
    status = django_filters.ChoiceFilter(choices=get_interview_status_choices())

    search = django_filters.CharFilter(
        method='filter_search',
        label='Search in title and description',
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value)
        )

    class Meta:
        model = BimaHrTechnicalInterview
        fields = []