from django_filters import rest_framework as filters
from .models import User


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    is_approved = filters.BooleanFilter()
    is_active = filters.BooleanFilter()

    class Meta:
        model = User
        fields = ['name', 'email', 'is_approved', 'is_active']
