import django_filters
from core.abstract.views import AbstractViewSet
from .models import BimaErpProduct
from .serializers import BimaErpProductSerializer

from .utils import generate_xls_file, export_to_csv
from common.utils.utils import render_to_pdf
from django.db import models


class ProductFilter(django_filters.FilterSet):
    category = django_filters.UUIDFilter(field_name='category__public_id')
    vat = django_filters.UUIDFilter(field_name='vat__public_id')
    unit_of_measure = django_filters.UUIDFilter(field_name='unit_of_measure__public_id')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type')
    low_stock = django_filters.BooleanFilter(method='low_stock_filter')

    class Meta:
        model = BimaErpProduct
        fields = ['name', 'type', 'reference', 'status', 'serial_number', 'category', 'vat', 'unit_of_measure']

    def low_stock_filter(self, queryset, name, value):
        if value:
            return queryset.filter(quantity__lte=models.F('minimum_stock_level'))
        return queryset


class BimaErpProductViewSet(AbstractViewSet):
    queryset = BimaErpProduct.objects.select_related('vat', 'category', 'unit_of_measure').all()
    serializer_class = BimaErpProductSerializer
    ordering_fields = AbstractViewSet.ordering_fields + ['reference', 'name', 'type', 'sell_price', 'status']
    permission_classes = []
    filterset_class = ProductFilter

    def get_object(self):
        obj = BimaErpProduct.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj

    def export_csv(self, request, **kwargs):
        data_to_export = self.get_data_to_export(kwargs)
        model_fields = BimaErpProduct._meta
        return export_to_csv(data_to_export, model_fields)

    def export_pdf(self, request, **kwargs):
        template_name = "product/pdf.html"
        data_to_export = self.get_data_to_export(kwargs)
        return render_to_pdf(
            template_name,
            {
                "products": data_to_export,
            },
            "product.pdf"
        )

    def export_xls(self, request, **kwargs):
        model_fields = BimaErpProduct._meta
        data_to_export = self.get_data_to_export(kwargs)
        return generate_xls_file(data_to_export, model_fields)

    def get_data_to_export(self, kwargs):
        if kwargs.get('public_id') is not None:
            data_to_export = [BimaErpProduct.objects.
                              get_object_by_public_id(kwargs.get('public_id'))]
        else:
            data_to_export = BimaErpProduct.objects.all()
        return data_to_export
