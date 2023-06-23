import os
from uuid import UUID

import django_filters
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum, Q
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from core.abstract.views import AbstractViewSet
from ..product.models import BimaErpProduct
from .models import BimaErpSaleDocument, BimaErpSaleDocumentProduct, update_sale_document_totals
from .serializers import BimaErpSaleDocumentSerializer, BimaErpSaleDocumentProductSerializer, \
    BimaErpSaleDocumentHistorySerializer, BimaErpSaleDocumentProductHistorySerializer

from common.service.purchase_sale_service import generate_unique_number
from common.enums.sale_document_enum import SaleDocumentStatus, get_sale_document_recurring_interval
from common.utils.utils import render_to_pdf

from common.enums.sale_document_enum import SaleDocumentValidity


class SaleDocumentFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(field_name='number', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')
    partner = django_filters.CharFilter(method='filter_partner_hex')
    date_gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    validity_expired = django_filters.BooleanFilter(method='filter_validity_expired')

    class Meta:
        model = BimaErpSaleDocument
        fields = ['number', 'status', 'type', 'partner', 'date_gte', 'date_lte', 'total_amount_gte', 'total_amount_lte',
                  'validity_expired']

    def filter_validity_expired(self, queryset, name, value):
        current_date = timezone.now().date()
        validity_days = {validity.name: int(validity.name.split("_")[1]) for validity in SaleDocumentValidity}

        if value is 'ALL':  # If value is not provided, return all documents
            return queryset

        queries = Q()
        for validity, days in validity_days.items():
            if value is 'EXPIRED':  # If value is True, the document is expired
                queries |= Q(date__lte=current_date - timedelta(days=days), validity=validity)
            elif value is 'NOT_EXPIRED':  # If value is False, the document is not expired
                queries |= Q(date__gt=current_date - timedelta(days=days), validity=validity)

        return queryset.filter(queries)

    def filter_partner_hex(self, queryset, name, value):
        try:
            uuid_value = UUID(hex=value)
            return queryset.filter(partner__public_id=uuid_value)
        except ValueError:
            return queryset

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
            return Response({'error': _('Please provide all needed data')},
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
            return Response({'error': _('Mismatched sale_document_id')},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        sale_document_product = get_list_or_404(BimaErpSaleDocumentProduct,
                                                sale_document__public_id=sale_document_public_id, product=product)[0]
        if sale_document_product is None:
            return Response({'error': _('Cannot find the item to edit')}, status=status.HTTP_404_NOT_FOUND)

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
            return Response({'error': _('Mismatched sale_document_id')},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        sale_document_product = get_object_or_404(BimaErpSaleDocumentProduct,
                                                  sale_document__public_id=sale_document_public_id, product=product)
        sale_document_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    @action(detail=False, methods=['post'])
    def create_new_document_from_parent(self, request, *args, **kwargs):
        document_type, parent_public_ids = self.get_request_data(request)
        parents = self.get_parents(parent_public_ids)

        self.validate_parents(parents)
        self.validate_document_type(document_type)

        new_document = create_new_document(document_type, parents)
        reset_quantity = True if document_type.lower() == 'credit_note' else False
        self.create_products_from_parents(parents, new_document, reset_quantity)

        return Response({"success": _("Item created")}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='get_history_diff')
    def get_history_diff(self, request, pk=None):
        sale_document = self.get_object()

        history = list(sale_document.history.all())

        if len(history) < 2:
            return Response({'error': 'Not enough history to compare.'}, status=status.HTTP_400_BAD_REQUEST)

        changes_by_date = {}
        for i in range(len(history) - 1):
            latest_history = history[i]
            previous_history = history[i + 1]

            latest_serialized = BimaErpSaleDocumentHistorySerializer(latest_history).data
            previous_serialized = BimaErpSaleDocumentHistorySerializer(previous_history).data

            for field, latest_value in latest_serialized.items():
                if field == 'history_date':
                    continue

                previous_value = previous_serialized.get(field)
                if latest_value != previous_value:
                    change_date = latest_serialized.get('history_date')
                    change = {
                        'field': field,
                        'old_value': previous_value,
                        'new_value': latest_value
                    }

                    # Group changes by date
                    if change_date in changes_by_date:
                        changes_by_date[change_date].append(change)
                    else:
                        changes_by_date[change_date] = [change]

        ordered_changes = [{'date': date, 'changes': changes} for date, changes in changes_by_date.items()]

        return Response({'differences': ordered_changes}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='get_product_history_diff')
    def get_product_history_diff(self, request, pk=None):
        sale_document = self.get_object()

        # Query the historical records directly
        history_records = BimaErpSaleDocumentProduct.history.filter(sale_document_id=sale_document.id).order_by(
            'history_date')

        # Group history records by product_id
        history_by_product = defaultdict(list)
        for record in history_records:
            history_by_product[record.sale_document_public_id].append(record)

        all_products_differences = []
        for product_public_id, history in history_by_product.items():
            if len(history) < 2:
                continue

            changes_by_date = {}
            for i in range(len(history) - 1):
                latest_history = history[i]
                previous_history = history[i + 1]

                latest_serialized = BimaErpSaleDocumentProductHistorySerializer(latest_history).data
                previous_serialized = BimaErpSaleDocumentProductHistorySerializer(previous_history).data

                for field, latest_value in latest_serialized.items():
                    # Ignore the history_date and history_type fields
                    if field in ['history_date', 'history_type', 'id']:
                        continue

                    previous_value = previous_serialized.get(field)
                    if latest_value != previous_value:
                        change_date = latest_serialized.get('history_date')
                        history_type = latest_serialized.get('history_type')
                        change = {
                            'field': field,
                            'old_value': previous_value,
                            'new_value': latest_value,
                            'history_type': history_type
                        }

                        # Group changes by date
                        if change_date in changes_by_date:
                            changes_by_date[change_date].append(change)
                        else:
                            changes_by_date[change_date] = [change]

            # Convert changes_by_date to an ordered list
            ordered_changes = [{'date': date, 'changes': changes} for date, changes in changes_by_date.items()]

            product_name = history[0].name if history else None
            all_products_differences.append({
                'product_name': product_name,
                'differences': ordered_changes
            })

        return Response({'products_differences': all_products_differences}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='generate_pdf')
    def generate_pdf(self, request, pk=None):
        sale_document = self.get_object()
        partner = sale_document.partner

        return render_to_pdf('sale_document/sale_document.html',
                             {'sale_document': sale_document, 'partner': partner},
                             "document.pdf")

    @transaction.atomic
    @action(detail=False, methods=['get'], url_path='generate_recurring_sale_documents', permission_classes=[])
    def generate_recurring_sale_documents(self, request):

        authorization_token = request.headers.get('Authorization')
        expected_token = os.environ.get('AUTHORIZATION_TOKEN_FOR_CRON')

        if authorization_token != expected_token:
            return JsonResponse({'error': _('Unauthorized')}, status=401)

        today = datetime.today()
        num_new_sale_documents = 0

        recurring_sale_documents = BimaErpSaleDocument.objects.filter(is_recurring=True)

        logger = logging.getLogger(__name__)

        for sale_document in recurring_sale_documents:
            next_creation_date = sale_document.date + timedelta(days=sale_document.recurring_interval)

            if next_creation_date <= today:
                try:
                    with transaction.atomic():
                        new_sale_document = create_new_document(
                            document_type=sale_document.type,
                            parents=[sale_document]
                        )
                        self.create_products_from_parents(parents=[sale_document], new_document=new_sale_document)

                        logger.info(
                            f"{new_sale_document.type} N° {new_sale_document.number}"
                            f" is created from {sale_document.number}")

                        num_new_sale_documents += 1

                except Exception as e:
                    logger.error(_(f"Error creating new SaleDocument for parent {sale_document.id}: {str(e)}"))

        return JsonResponse({'message': _(f'Successfully created {num_new_sale_documents} new sale documents')})

    def get_request_data(self, request):
        document_type = request.data.get('document_type', '')
        parent_public_ids = request.data.get('parent_public_ids', [])
        return document_type, parent_public_ids

    def get_parents(self, parent_public_ids):
        return BimaErpSaleDocument.objects.filter(public_id__in=parent_public_ids)

    def validate_parents(self, parents):
        if not parents.exists():
            raise ValidationError({'error': _('No valid parent documents found')})
        unique_partners = parents.values('partner').distinct()
        if len(unique_partners) > 1:
            raise ValidationError({'error': _('All documents should belong to the same partner')})

    def validate_document_type(self, document_type):
        if not document_type:
            raise ValidationError({'error': _('Please give the type of the document')})

    def create_products_from_parents(self, parents, new_document, reset_quantity=False):
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
                unit_of_measure=first_product.unit_of_measure,
                reference=first_product.reference,
                product_id=product_id,
                quantity=1 if reset_quantity else total_quantity,
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
