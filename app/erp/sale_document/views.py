from datetime import datetime
import django_filters
from core.abstract.views import AbstractViewSet
from core.abstract.base_filter import BaseFilter
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.response import Response

from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct, update_sale_document_totals
from .serializers import BimaErpSaleDocumentSerializer, BimaErpSaleDocumentProductSerializer
from common.service.purchase_sale_service import generate_unique_number
from common.enums.sale_document_enum import SaleDocumentStatus

from ..product.models import BimaErpProduct


class SaleDocumentFilter(BaseFilter):
    partner_name = django_filters.CharFilter(field_name='partner__name', lookup_expr='icontains')
    number = django_filters.CharFilter(field_name='number', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='icontains')
    type = django_filters.CharFilter(field_name='type', lookup_expr='exact')

    class Meta:
        model = BimaErpSaleDocument
        fields = ['number', 'status', 'partner_name', 'type']


def create_new_document(document_type, parents):
    new_document = BimaErpSaleDocument.objects.create(
        number=generate_unique_number('sale', document_type.lower()),
        date=datetime.today().strftime('%Y-%m-%d'),
        status=SaleDocumentStatus.DRAFT,
        type=document_type,
        partner=parents.first().partner,
    )
    new_document.parents.add(*parents)
    return new_document


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

    from django.db.models import F
    from rest_framework.decorators import action

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def create_new_document_from_parent(self, request, *args, **kwargs):
        document_type, parent_public_ids = self.get_request_data(request)
        parents = self.get_parents(parent_public_ids)

        # Validation checks
        self.validate_parents(parents)
        self.validate_document_type(document_type)

        # Creation of new document
        new_document = create_new_document(document_type, parents)

        # Get product aggregates and create new products for the new document
        self.create_products_from_parents(parents, new_document)

        serializer = BimaErpSaleDocumentSerializer(new_document)
        return Response({"success": "Item created"}, status=status.HTTP_201_CREATED)

    def get_request_data(self, request):
        document_type = request.data.get('document_type', '')
        parent_public_ids = request.data.get('parent_public_ids', [])
        return document_type, parent_public_ids

    def get_parents(self, parent_public_ids):
        return BimaErpSaleDocument.objects.filter(public_id__in=parent_public_ids)

    def validate_parents(self, parents):
        if not parents.exists():
            raise ValidationError({'error': 'No valid parent documents found'})
        unique_partners = parents.values('partner').distinct()
        if len(unique_partners) > 1:
            raise ValidationError({'error': 'All documents should belong to the same partner'})

    def validate_document_type(self, document_type):
        if not document_type:
            raise ValidationError({'error': 'Please give the type of the document'})

    def create_products_from_parents(self, parents, new_document):
        product_ids = BimaErpSaleDocumentProduct.objects.filter(
            sale_document__in=parents
        ).values_list('product', flat=True).distinct()

        new_products = []
        for product_id in product_ids:
            # Find first instance of this product
            first_product = BimaErpSaleDocumentProduct.objects.filter(
                sale_document__in=parents,
                product_id=product_id
            ).first()

            if first_product is None:
                continue

            total_quantity = BimaErpSaleDocumentProduct.objects.filter(
                sale_document__in=parents,
                product_id=product_id
            ).aggregate(total_quantity=Sum('quantity'))['total_quantity']


            new_product = BimaErpSaleDocumentProduct(
                sale_document=new_document,
                name=first_product.name,
                reference=first_product.reference,
                product_id=product_id,
                quantity=total_quantity,
                unit_price=first_product.unit_price,
                vat=first_product.vat,
                description=first_product.description,
                discount=first_product.discount
            )
            new_product.calculate_totals()
            new_products.append(new_product)

        BimaErpSaleDocumentProduct.objects.bulk_create(new_products)
        update_sale_document_totals(new_document)
        new_document.save()
