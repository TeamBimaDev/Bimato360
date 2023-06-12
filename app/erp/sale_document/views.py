import django_filters
from core.abstract.views import AbstractViewSet
from core.abstract.base_filter import BaseFilter
from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from .serializers import BimaErpSaleDocumentSerializer, SaleDocumentProductSerializer
from common.service.purchase_sale_service import generate_unique_number


class SaleDocumentFilter(BaseFilter):
    partner_name = django_filters.CharFilter(field_name='partner__name', lookup_expr='icontains')
    number = django_filters.CharFilter(field_name='number', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')

    class Meta:
        model = BimaErpSaleDocument
        fields = ['number', 'status', 'partner_name']


class BimaErpSaleDocumentViewSet(AbstractViewSet):
    queryset = BimaErpSaleDocument.objects.select_related('partner').all()
    serializer_class = BimaErpSaleDocumentSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []
    filterset_class = SaleDocumentFilter

    def get_object(self):
        obj = BimaErpSaleDocument.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def get_unique_number(self, request, **kwargs):
        sale_or_purchase = kwargs.get('sale_purchase', '')
        quotation_order_invoice = kwargs.get('quotation_order_invoice', '')

        if not sale_or_purchase or not quotation_order_invoice:
            return HttpResponseBadRequest("Please provide all needed data.")

        unique_number = generate_unique_number(sale_or_purchase, quotation_order_invoice)
        while BimaErpSaleDocument.objects.filter(numbers=unique_number).exists():
            unique_number = generate_unique_number(sale_or_purchase, quotation_order_invoice)
        return Response({"unique_number": unique_number})

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        serializer = SaleDocumentProductSerializer(data=request.data, context={'sale_document_public_id': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_product(self, request, pk=None):
        sale_document_product = BimaErpSaleDocumentProduct.objects.get(pk=pk)
        serializer = SaleDocumentProductSerializer(sale_document_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        sale_document_product = BimaErpSaleDocumentProduct.objects.get(pk=pk)
        sale_document_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
