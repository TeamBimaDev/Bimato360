import django_filters
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.abstract.views import AbstractViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import BimaErpProduct
from .serializers import BimaErpProductSerializer
from .utils import generate_xls_file, export_to_csv, read_barcode_from_image, generate_file, enhance_image
from common.utils.utils import render_to_pdf
from erp.sale_document.models import BimaErpSaleDocumentProduct
from core.entity_tag.models import get_entity_tags_for_parent_entity, create_single_entity_tag, BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from common.permissions.action_base_permission import ActionBasedPermission
import barcode
from barcode.writer import ImageWriter
from django.http import  JsonResponse
import numpy as np
import io
from PIL import Image

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
                "request": request,
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
    @action(detail=False, methods=['POST'], url_path='generate_ena13_from_image')
    def generate_ena13_from_image(self, request):
        barcode_image = request.FILES.get('barcode_image')
        if not barcode_image:
            return JsonResponse({'error': 'Missing barcode_image field in the request.'}, status=400)
        img_array = np.asarray(bytearray(barcode_image.read()), dtype=np.uint8)
        image = Image.open(io.BytesIO(img_array))
        enhanced_image = enhance_image(image)
        enhanced_image = enhanced_image.convert('L')
        enhanced_np_array = np.array(enhanced_image)
        decoded_data = read_barcode_from_image(np.array(enhanced_np_array))

        if decoded_data:
            bar = barcode.get_barcode(name='code128', code=decoded_data, writer=ImageWriter())
            barcode_file = bar.render()
            generated_text = decoded_data

            return JsonResponse({'generated_text': generated_text})
        else:
            return JsonResponse({'error': 'No barcode found in the image.'}, status=400)

    def verify_file_exist_for_ean13(request):
        barcode_image = request.FILES.get('barcode_image')
        if not barcode_image:
            raise ValueError("File is missing or unable to read the file")
        return barcode_image
