import csv

from core.abstract.views import AbstractViewSet
from django.db.models import prefetch_related_objects
from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import BimaErpProduct
from .serializers import BimaErpProductSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination

from erp.category.models import BimaErpCategory
from erp.unit_of_measure.models import BimaErpUnitOfMeasure
from erp.vat.models import BimaErpVat
from django_filters import rest_framework as filters


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = BimaErpProduct
        fields = ['name', 'category_name', 'type']


def get_category_vat_unit_of_measure_from_query(data_to_save):
    category_public_id = data_to_save.get('category')
    vat_public_id = data_to_save.get('vat')
    unit_of_measure_public_id = data_to_save.get('unit_of_measure')

    category = get_object_or_404(BimaErpCategory, public_id=category_public_id)
    vat = get_object_or_404(BimaErpVat, public_id=vat_public_id)
    unit_of_measure = get_object_or_404(BimaErpUnitOfMeasure, public_id=unit_of_measure_public_id)

    data_to_save['category_id'] = category.id
    data_to_save['vat_id'] = vat.id
    data_to_save['unit_of_measure_id'] = unit_of_measure.id
    return data_to_save


class BimaErpProductViewSet(AbstractViewSet):
    queryset = BimaErpProduct.objects.select_related('vat', 'category', 'unit_of_measure').all()
    serializer_class = BimaErpProductSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []
    pagination_class = DefaultPagination
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        data_to_save = get_category_vat_unit_of_measure_from_query(request.data)
        serializer = self.get_serializer(data=data_to_save)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = get_category_vat_unit_of_measure_from_query(request.data)
        serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaErpProduct.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj

    def export_data_csv(self, request, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="partners.csv"'
        model_fields = BimaErpProduct._meta
        field_names_to_show = [fd.name for fd in model_fields.fields]
        writer = csv.writer(response)
        writer.writerow(field_names_to_show)
        if kwargs.get('public_id') is not None:
            data_to_export = [BimaErpProduct.objects.
                              get_object_by_public_id(kwargs.get('public_id'))]
        else:
            data_to_export = BimaErpProduct.objects.all()

        for partner in data_to_export:
            writer.writerow([getattr(partner, field) for field in field_names_to_show])

        return response
