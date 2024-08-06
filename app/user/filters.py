from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    is_approved = filters.CharFilter(method='filter_is_approved')
    is_active = filters.CharFilter(method='filter_is_active')

    class Meta:
        model = get_user_model()
        fields = ['name', 'email', 'is_approved', 'is_active']

    def filter_is_approved(self, queryset, name, value):
        if value.lower() in ['true', 'false']:
            return queryset.filter(is_approved=value.lower() == 'true')
        return queryset

    def filter_is_active(self, queryset, name, value):
        if value.lower() in ['true', 'false']:
            return queryset.filter(is_active=value.lower() == 'true')
        return queryset
