import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.abstract.views import AbstractViewSet
from django.shortcuts import get_object_or_404
from pandas import read_csv
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import BimaErpProduct
from .serializers import BimaErpProductSerializer
from .utils import generate_xls_file, export_to_csv, verify_file_exist_for_ean13, generate_ean13_from_image, \
    import_product_data_from_csv_file
from common.utils.utils import render_to_pdf
from erp.sale_document.models import BimaErpSaleDocumentProduct
from core.entity_tag.models import get_entity_tags_for_parent_entity, create_single_entity_tag, BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from common.permissions.action_base_permission import ActionBasedPermission

from django.http import JsonResponse

import logging

from common.service.file_service import check_csv_file

logger = logging.getLogger(__name__)


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact')
    reference = django_filters.CharFilter(field_name='reference', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    serial_number = django_filters.CharFilter(field_name='serial_number', lookup_expr='icontains')
    category = django_filters.UUIDFilter(field_name='category__public_id')
    vat = django_filters.UUIDFilter(field_name='vat__public_id')
    unit_of_measure = django_filters.UUIDFilter(field_name='unit_of_measure__public_id')
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
    permission_classes = (ActionBasedPermission,)
    filterset_class = ProductFilter
    action_permissions = {
        'list': ['product.can_read'],
        'export_csv': ['product.can_read'],
        'export_xls': ['product.can_read'],
        'export_pdf': ['product.can_read'],
        'create': ['product.can_create'],
        'generate_ena13_from_image': ['product.can_create'],
        'retrieve': ['product.can_read'],
        'update': ['product.can_update'],
        'partial_update': ['product.can_update'],
        'destroy': ['product.can_delete'],
    }

    def get_object(self):
        obj = BimaErpProduct.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj

    def list_tags(self, request, *args, **kwargs):
        product = BimaErpProduct.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_entity_tags_for_parent_entity(product).order_by('order')
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if BimaErpSaleDocumentProduct.objects.filter(product=instance).exists():
            return Response({"Error": _("Item exists in a sale document")}, status=status.HTTP_400_BAD_REQUEST)

        return super(BimaErpProductViewSet, self).destroy(request, *args, **kwargs)

    def create_tag(self, request, *args, **kwargs):
        product = BimaErpProduct.objects.get_object_by_public_id(self.kwargs['public_id'])
        result = create_single_entity_tag(request.data, product)
        if isinstance(result, BimaCoreEntityTag):
            serializer = BimaCoreEntityTagSerializer(result)
            return Response({
                "id": result.public_id,
                "tag_name": result.tag.name,
                "order": result.order
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_tag(self, request, *args, **kwargs):
        product = BimaErpProduct.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_object_or_404(BimaCoreEntityTag,
                                        public_id=self.kwargs['entity_tag_public_id'],
                                        parent_id=product.id)
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags)
        return JsonResponse(serialized_entity_tags.data)

    @action(detail=False, methods=['POST'], url_path='generate_ena13_from_image')
    def generate_ena13_from_image(self, request):
        try:
            barcode_image = verify_file_exist_for_ean13(request)
            response, status_code = generate_ean13_from_image(barcode_image)
            return Response(response, status=status_code)
        except ValidationError as ex:
            logger.error(f'Validation error while generating barcode from file: {str(ex)}')
            return Response({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], url_path='import_from_csv')
    def import_from_csv(self, request):
        csv_file = request.FILES.get('csv_file')

        try:
            file_check = check_csv_file(csv_file)
            if 'error' in file_check:
                return Response(file_check, status=status.HTTP_400_BAD_REQUEST)

            csv_content_file = read_csv(csv_file)

            error_rows, created_count = import_product_data_from_csv_file(csv_content_file)
            if error_rows:
                return Response({
                    'error': _('Some rows could not be processed'),
                    'error_rows': error_rows,
                    'success_rows_count': created_count,
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': _('All rows processed successfully'),
                             'success_rows_count': created_count})

        except Exception:
            return Response({"error", _("an error occurred while treating the file")},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], url_path='export_csv')
    def export_csv(self, request):
        data_to_export = self.get_queryset()
        model_fields = BimaErpProduct._meta
        return export_to_csv(data_to_export, model_fields)

    @action(detail=False, methods=['GET'], url_path='export_pdf')
    def export_pdf(self, request):
        template_name = "product/pdf.html"
        data_to_export = self.get_queryset()
        return render_to_pdf(
            template_name,
            {
                "products": data_to_export,
                "request": request,
            },
            "product.pdf"
        )

    @action(detail=False, methods=['GET'], url_path='export_xls')
    def export_xls(self, request):
        model_fields = BimaErpProduct._meta
        data_to_export = self.get_queryset()
        return generate_xls_file(data_to_export, model_fields)

    @action(detail=True, methods=['GET'], url_path='export_csv')
    def detail_export_csv(self, request, pk=None):
        data_to_export = [self.get_object()]
        model_fields = BimaErpProduct._meta
        return export_to_csv(data_to_export, model_fields)

    @action(detail=True, methods=['GET'], url_path='export_pdf')
    def detail_export_pdf(self, request, pk=None):
        template_name = "product/pdf.html"
        data_to_export = [self.get_object()]
        return render_to_pdf(
            template_name,
            {
                "products": data_to_export,
                "request": request,
            },
            "product.pdf"
        )

    @action(detail=True, methods=['GET'], url_path='export_xls')
    def detail_export_xls(self, request, pk=None):
        model_fields = BimaErpProduct._meta
        data_to_export = [self.get_object()]
        return generate_xls_file(data_to_export, model_fields)
