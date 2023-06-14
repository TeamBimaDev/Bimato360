import csv
import django_filters
from core.abstract.views import AbstractViewSet
from django.http import HttpResponse
from .models import BimaErpProduct
from .serializers import BimaErpProductSerializer
from core.abstract.base_filter import BaseFilter


class ProductFilter(BaseFilter):
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='exact')
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = BimaErpProduct
        fields = ['category_name', 'type', 'name']


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
