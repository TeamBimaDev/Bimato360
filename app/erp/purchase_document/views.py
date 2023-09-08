from collections import defaultdict
from itertools import groupby

from common.enums.sale_document_enum import get_sale_document_status, get_sale_document_types
from common.permissions.action_base_permission import ActionBasedPermission
from common.utils.utils import render_to_pdf
from company.models import BimaCompany
from company.service import fetch_company_data
from core.abstract.pagination import DefaultPagination
from core.abstract.views import AbstractViewSet
from core.address.models import BimaCoreAddress
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.translation import gettext_lazy as _
from erp.product.models import BimaErpProduct
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filter import PurchaseDocumentFilter
from .models import BimaErpPurchaseDocument, BimaErpPurchaseDocumentProduct
from .serializers import BimaErpPurchaseDocumentSerializer, BimaErpPurchaseDocumentProductSerializer, \
    BimaErpPurchaseDocumentHistorySerializer, BimaErpPurchaseDocumentProductHistorySerializer
from .service import PurchaseDocumentService, create_products_from_parents, generate_xls_report, generate_csv_report, \
    calculate_totals_for_selected_items, create_new_document
from .service_payment_invoice import handle_invoice_payment
from .service_payment_notification import verify_purchase_document_payment_status


class BimaErpPurchaseDocumentViewSet(AbstractViewSet):
    queryset = BimaErpPurchaseDocument.objects.select_related('partner').all()
    serializer_class = BimaErpPurchaseDocumentSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = ['number', 'date', 'status', 'partner__name', 'total_amount']
    ordering = ['date']
    filterset_class = PurchaseDocumentFilter
    action_permissions = {
        'list': ['purchase_document.can_read'],
        'create': ['purchase_document.can_create'],
        'retrieve': ['purchase_document.can_read'],
        'update': ['purchase_document.can_update'],
        'partial_update': ['purchase_document.can_update'],
        'destroy': ['purchase_document.can_delete'],
        'get_history_diff': ['purchase_document.can_view_history'],
        'get_product_history_diff': ['purchase_document.can_view_history'],
        'generate_pdf': ['purchase_document.can_generate_document'],
        'request_for_quotation': ['purchase_document.can_generate_document'],

    }

    def get_object(self):
        obj = BimaErpPurchaseDocument.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('status')

        if instance.status == 'DRAFT' and new_status in ['CONFIRMED', 'CANCELED']:
            if not request.user.has_perm('erp.purchase_document.can_change_status'):
                return Response({'error': _('You do not have permission to change the status')},
                                status=status.HTTP_403_FORBIDDEN)
        elif instance.status in ['CONFIRMED', 'CANCELED'] and new_status == 'DRAFT':
            if not request.user.has_perm('erp.purchase_document.can_rollback_status'):
                return Response({'error': _('You do not have permission to rollback the status')},
                                status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        new_status = request.data.get('status')

        if new_status in ['CONFIRMED', 'CANCELED']:
            if not request.user.has_perm('erp.purchase_document.can_change_status'):
                return Response({'error': _('You do not have permission to set the status')},
                                status=status.HTTP_403_FORBIDDEN)

        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def get_unique_number(self, request, **kwargs):
        try:
            unique_number = PurchaseDocumentService.get_unique_number(request, **kwargs)
            return Response({"unique_number": unique_number})
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='products')
    def get_products(self, request, pk=None):
        purchase_document = self.get_object()
        products = BimaErpPurchaseDocumentProduct.objects.filter(purchase_document=purchase_document)
        serializer = BimaErpPurchaseDocumentProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_product(self, request, pk=None):
        purchase_document = self.get_object()
        serializer = BimaErpPurchaseDocumentProductSerializer(data=request.data,
                                                              context={'purchase_document': purchase_document})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_product(self, request, pk=None):
        purchase_document_public_id = request.data.get('purchase_document_public_id')
        product_public_id = request.data.get('product_public_id')

        if pk != purchase_document_public_id:
            return Response({'error': _('Mismatched purchase_document_id')},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        purchase_document_product = get_list_or_404(BimaErpPurchaseDocumentProduct,
                                                    purchase_document__public_id=purchase_document_public_id,
                                                    product=product)[0]
        if purchase_document_product is None:
            return Response({'error': _('Cannot find the item to edit')}, status=status.HTTP_404_NOT_FOUND)

        serializer = BimaErpPurchaseDocumentProductSerializer(purchase_document_product, data=request.data,
                                                              partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_product(self, request, pk=None):
        purchase_document_public_id = request.data.get('purchase_document_public_id')
        product_public_id = request.data.get('product_public_id')

        if pk != purchase_document_public_id:
            return Response({'error': _('Mismatched purchase_document_id')},
                            status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        purchase_document_product = get_object_or_404(BimaErpPurchaseDocumentProduct,
                                                      purchase_document__public_id=purchase_document_public_id,
                                                      product=product)
        purchase_document_product.delete()
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
        create_products_from_parents(parents, new_document, reset_quantity)

        return Response({"success": _("Item created")}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='get_history_diff')
    def get_history_diff(self, request, pk=None):
        purchase_document = self.get_object()

        history = list(purchase_document.history.all().select_related('history_user').order_by('-history_date'))

        if len(history) < 2:
            return Response([], status=status.HTTP_200_OK)

        changes_by_date = {}
        for i in range(len(history) - 1):
            previous_history = history[i]
            latest_history = history[i + 1]

            latest_serialized = BimaErpPurchaseDocumentHistorySerializer(latest_history).data
            previous_serialized = BimaErpPurchaseDocumentHistorySerializer(previous_history).data

            for field, latest_value in latest_serialized.items():
                if field == 'history_date':
                    continue

                previous_value = previous_serialized.get(field)
                if latest_value != previous_value:
                    change_date = latest_serialized.get('history_date')
                    change = {
                        'field': field,
                        'old_value': latest_value,
                        'new_value': previous_value,
                        'user': previous_history.history_user.name if previous_history.history_user else None
                    }

                    if change_date in changes_by_date:
                        changes_by_date[change_date].append(change)
                    else:
                        changes_by_date[change_date] = [change]

        ordered_changes = [{'date': date, 'changes': changes} for date, changes in changes_by_date.items()]

        return Response({'differences': ordered_changes}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='get_product_history_diff')
    def get_product_history_diff(self, request, pk=None):
        purchase_document = self.get_object()

        history_records = BimaErpPurchaseDocumentProduct.history.filter(
            purchase_document_id=purchase_document.id).order_by(
            '-history_date')

        history_by_product = defaultdict(list)
        for record in history_records:
            history_by_product[record.product_id].append(record)

        all_products_differences = []
        for product_id, history in history_by_product.items():
            history = sorted(history, key=lambda x: x.history_date)

            product_differences = []
            for i in range(len(history) - 1):
                previous_history = history[i]
                latest_history = history[i + 1]

                latest_serialized = BimaErpPurchaseDocumentProductHistorySerializer(latest_history).data
                previous_serialized = BimaErpPurchaseDocumentProductHistorySerializer(previous_history).data

                for field, latest_value in latest_serialized.items():
                    if field in ['history_date', 'history_type', 'id']:
                        continue

                    previous_value = previous_serialized.get(field)
                    if latest_value != previous_value:
                        change = {
                            'date': latest_serialized.get('history_date'),
                            'field': field,
                            'old_value': previous_value,
                            'new_value': latest_value,
                            'history_type': latest_serialized.get('history_type'),
                            'user': latest_history.history_user.name if latest_history.history_user else None
                        }
                        product_differences.append(change)

            product_name = history[0].name if history else None

            product_differences.sort(key=lambda x: x['date'])

            grouped_product_differences = []
            for key, group in groupby(product_differences, lambda x: x['date']):
                grouped_product_differences.append({
                    'date': key,
                    'changes': list(group)
                })

            all_products_differences.append({
                'product_id': product_id,
                'product_name': product_name,
                'differences': grouped_product_differences
            })

        return Response({'products_differences': all_products_differences}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='generate_pdf')
    def generate_pdf(self, request, pk=None):
        pdf_filename = "document.pdf"
        context = self._get_context(pk)
        context['document_title'] = context['current_document'].display_type
        context['translated_status'] = dict(get_sale_document_status()).get(context['current_document'].status)
        context['translated_type'] = dict(get_sale_document_types()).get(context['current_document'].type)
        context['request'] = request
        company_data = context.get('company_data', None)
        default_sale_document_pdf_format = company_data.get('default_sale_document_pdf_format')
        template_name = f'sale_document/sale_templates/{default_sale_document_pdf_format}'
        return render_to_pdf(template_name, context, pdf_filename)

    @action(detail=True, methods=['get'], url_path='request_for_quotation')
    def request_for_quotation(self, request, pk=None):
        pdf_filename = "document.pdf"
        context = self._get_context(pk)
        context['document_title'] = str(_('Request for Quotation'))
        context['translated_status'] = dict(get_sale_document_status()).get(context['current_document'].status)
        context['translated_type'] = str(_('Request for Quotation'))
        context['request'] = request
        context['show_price'] = False
        company_data = context.get('company_data', None)
        default_sale_document_pdf_format = company_data.get('default_sale_document_pdf_format')
        template_name = f'sale_document/sale_templates/{default_sale_document_pdf_format}'
        return render_to_pdf(template_name, context, pdf_filename)

    @action(detail=False, methods=['GET'], url_path='generate_pdf_resume')
    def generate_pdf_resume(self, request):
        template_name = 'sale_document/sale_document_resume.html'
        pdf_filename = 'resume.pdf'
        context = self._get_context_resume(request)
        context['document_title'] = _("Rapport")
        context['request'] = request
        return render_to_pdf(template_name, context, pdf_filename)

    @action(detail=False, methods=['GET'], url_path='generate_xls_resume')
    def generate_xls_resume(self, request):
        model_fields = BimaErpPurchaseDocument._meta.fields
        data_to_export = self.get_filtered_data(request)
        return generate_xls_report(data_to_export, model_fields)

    @action(detail=False, methods=['GET'], url_path='generate_csv_resume')
    def generate_csv_resume(self, request):
        fields = BimaErpPurchaseDocument._meta.fields
        data_to_export = self.get_filtered_data(request)
        return generate_csv_report(data_to_export, fields)

    @action(detail=True, methods=['GET'], url_path='get_direct_parent')
    def get_direct_parent(self, request, pk=None):
        document = self.get_object()
        parents = document.parents
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='get_direct_child')
    def get_direct_child(self, request, pk):
        document = self.get_object()
        paginator = DefaultPagination()
        child = paginator.paginate_queryset(document.bimaerppurchasedocument_set.all(), request)

        serializer = self.get_serializer(child, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST'], url_path="save_payment_with_transaction_credits")
    def save_payment_with_transaction_credits(self, request, pk=None):
        purchase_document = self.get_object()
        transaction_public_ids = self.request.data.pop('transaction_public_ids')
        handle_invoice_payment(purchase_document, transaction_public_ids)
        return Response({"Payment": _("Payement effectué avec succes")})

    @action(detail=False, methods=['GET'], url_path='verify_payment_status_purchase_document')
    def verify_payment_status_purchase_document(self, request, pk=None):
        return_data = verify_purchase_document_payment_status()
        return Response(return_data)

    def get_request_data(self, request):
        document_type = request.data.get('document_type', '')
        parent_public_ids = request.data.get('parent_public_ids', [])
        return document_type, parent_public_ids

    def get_parents(self, parent_public_ids):
        return BimaErpPurchaseDocument.objects.filter(public_id__in=parent_public_ids)

    def validate_parents(self, parents):
        if not parents.exists():
            raise ValidationError({'error': _('No valid parent documents found')})
        unique_partners = parents.values_list('partner__id', flat=True).distinct()
        unique_ids = list(set(unique_partners))
        if len(unique_ids) > 1:
            raise ValidationError({'error': _('All documents should belong to the same partner')})

    def validate_document_type(self, document_type):
        if not document_type:
            raise ValidationError({'error': _('Please give the type of the document')})

    def _get_context(self, pk=None):
        purchase_document = self.get_object()
        partner = purchase_document.partner

        partner_content_type = ContentType.objects.get_for_model(partner)
        first_address = BimaCoreAddress.objects.filter(
            parent_type=partner_content_type,
            parent_id=partner.id
        ).select_related('state', 'country').first()

        company = BimaCompany.objects.first()
        company_data = fetch_company_data(company)

        context = {'current_document': purchase_document, 'partner': partner, 'address': first_address,
                   'company_data': company_data, 'products': purchase_document.bimaerppurchasedocumentproduct_set.all}

        return context

    def _get_context_resume(self, request):
        purchase_documents = self.get_filtered_data(request)
        company = BimaCompany.objects.first()
        company_data = fetch_company_data(company)
        totals = calculate_totals_for_selected_items(purchase_documents)

        context = {'documents': purchase_documents, 'company_data': company_data, 'totals': totals}

        return context

    def get_filtered_data(self, request):
        queryset = BimaErpPurchaseDocument.objects.select_related('partner').all()
        filtered_sale_document = PurchaseDocumentFilter(request.GET, queryset=queryset)
        return filtered_sale_document.qs
