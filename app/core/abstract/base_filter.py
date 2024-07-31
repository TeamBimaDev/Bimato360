<<<<<<< HEAD
import django_filters
from django import forms
from django_filters import rest_framework as filters


class BaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        abstract = True



=======
import django_filters
from django import forms
from django_filters import rest_framework as filters


class BaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        abstract = True



>>>>>>> origin/ma-branch
