from datetime import datetime

import django_filters
from core.abstract.views import AbstractViewSet
from core.abstract.base_filter import BaseFilter
from django.db import transaction
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct
from .serializers import BimaErpSaleDocumentSerializer, BimaErpSaleDocumentProductSerializer
from common.service.purchase_sale_service import generate_unique_number

from common.enums.sale_document_enum import SaleDocumentStatus

from ..product.models import BimaErpProduct


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

    @action(detail=False, methods=['get'])
    def get_unique_number(self, request, **kwargs):
        sale_or_purchase = kwargs.get('sale_purchase', '')
        quotation_order_invoice = kwargs.get('quotation_order_invoice', '')
        if not sale_or_purchase:
            sale_or_purchase = request.query_params.get('sale_purchase', '')
        if not quotation_order_invoice:
            quotation_order_invoice = request.query_params.get('quotation_order_invoice', '')
        if not sale_or_purchase or not quotation_order_invoice:
            return Response({'error': 'Please provide all needed data'},
                            status=status.HTTP_400_BAD_REQUEST)

        unique_number = generate_unique_number(sale_or_purchase, quotation_order_invoice)
        while BimaErpSaleDocument.objects.filter(number=unique_number).exists():
            unique_number = generate_unique_number(sale_or_purchase, quotation_order_invoice)
        return Response({"unique_number": unique_number})

    @action(detail=True, methods=['get'], url_path='products')
    def get_products(self, request, pk=None):
        sale_document = self.get_object()
        products = BimaErpSaleDocumentProduct.objects.filter(sale_document=sale_document)
        serializer = BimaErpSaleDocumentProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        sale_document = self.get_object()
        serializer = BimaErpSaleDocumentProductSerializer(data=request.data, context={'sale_document': sale_document})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_product(self, request, pk=None):
        sale_document_public_id = request.data.get('sale_document_public_id')
        product_public_id = request.data.get('product_public_id')

        if pk != sale_document_public_id:
            return Response({'error': 'Mismatched sale_document_id'},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        sale_document_product = get_list_or_404(BimaErpSaleDocumentProduct,
                                                sale_document__public_id=sale_document_public_id, product=product)[0]
        if sale_document_product is None:
            return Response({'error': 'Cannot find the item to edit'}, status=status.HTTP_404_NOT_FOUND)

        serializer = BimaErpSaleDocumentProductSerializer(sale_document_product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        sale_document_public_id = request.data.get('sale_document_public_id')
        product_public_id = request.data.get('product_public_id')

        if pk != sale_document_public_id:
            return Response({'error': 'Mismatched sale_document_id'},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        sale_document_product = get_object_or_404(BimaErpSaleDocumentProduct,
                                                  sale_document__public_id=sale_document_public_id, product=product)
        sale_document_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def create_new_document_from_parent(self, request, *args, **kwargs):
        document_type = request.data.get('document_type', '')
        parent_public_ids = request.data.get('parent_public_ids', [])
        parents = BimaErpSaleDocument.objects.filter(public_id__in=parent_public_ids)
        if not parents.exists():
            return Response({'error': 'No valid parent documents found'}, status=status.HTTP_400_BAD_REQUEST)
        if not document_type:
            return Response({'error': 'Please give the type of the document'}, status=status.HTTP_400_BAD_REQUEST)

        unique_partners = parents.values_list('partner', flat=True).distinct()
        if len(unique_partners) > 1:
            return Response({'error': 'All documents should belong to the same partner'},
                            status=status.HTTP_400_BAD_REQUEST)

        new_document = BimaErpSaleDocument.objects.create(
            number=generate_unique_number('sale', 'invoice'),
            date=datetime.date.today(),
            status=SaleDocumentStatus.DRAFT,
            type=document_type,
            partner=parents.first().partner,

        )
        new_document.parents.add(*parents)

        product_agg = BimaErpSaleDocumentProduct.objects.filter(sale_document__in=parents).values('product').annotate(
            total_quantity=Sum('quantity')
        )
        for product in product_agg:
            total_price = product['unit_price'] * product['total_quantity']
            if product['vat']:
                total_price += (total_price * product['vat']) / 100
            if product['discount']:
                total_price -= (total_price * product['discount']) / 100

            BimaErpSaleDocumentProduct.objects.create(
                sale_document=new_document,
                name=product['name'],
                reference=product['reference'],
                product_id=product['product'],
                quantity=product['total_quantity'],
                unit_price=product['unit_price'],
                vat=product['vat'],
                description=product['description'],
                discount=product['discount'],
                total_price=total_price
            )

        serializer = BimaErpSaleDocumentSerializer(new_document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
