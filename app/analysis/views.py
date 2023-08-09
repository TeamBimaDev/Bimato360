from django.db import models
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from erp.partner.models import BimaErpPartner
from erp.sale_document.models import BimaErpSaleDocument
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class BimaAnalysisViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path="total_sales_report")
    def total_sales_report(self, request):
        partner_public_id = request.query_params.get('partner_public_id', None)
        filter_period = request.query_params.get("filter_period", 'monthly')

        if partner_public_id:
            partner = get_object_or_404(BimaErpPartner, public_id=partner_public_id)
        else:
            partner = None

        sales_documents = self._filter_sales_by_period(BimaErpSaleDocument.objects.all(), filter_period)
        all_sales_documents = sales_documents

        if partner:
            sales_documents = sales_documents.filter(partner__id=partner.id)

        aggregated_data = sales_documents.values('period').annotate(
            total_sales=models.Sum('total_amount'),
            transaction_count=models.Count('id'),
            avg_transaction_value=models.Avg('total_amount')
        ).order_by('period')

        # Calculating partner percentage and transaction percentage for each period
        if partner:
            for data in aggregated_data:
                period = data['period']

                # Calculate partner's percentage of sales and transaction for that specific period
                period_total_sales = \
                    all_sales_documents.filter(period=period).aggregate(total_sales=models.Sum('total_amount'))[
                        'total_sales']
                period_total_transactions = all_sales_documents.filter(period=period).count()

                period_sales_partner = \
                    sales_documents.filter(period=period).aggregate(total_sales=models.Sum('total_amount'))[
                        'total_sales']
                period_transaction_partner = sales_documents.filter(period=period).count()

                if period_total_sales:
                    data['partner_percentage'] = round((period_sales_partner / period_total_sales) * 100, 2)
                else:
                    data['partner_percentage'] = 0.0

                if period_total_transactions:
                    data['transaction_percentage_for_partner'] = round(
                        (period_transaction_partner / period_total_transactions) * 100, 2)
                else:
                    data['transaction_percentage_for_partner'] = 0.0

            return Response({'aggregated_data': aggregated_data}, status=status.HTTP_200_OK)
        else:
            return Response({'aggregated_data': aggregated_data}, status=status.HTTP_200_OK)

    def _filter_sales_by_period(self, queryset, filter_period):
        """Filter sales documents by period."""
        if filter_period == 'daily':
            return queryset.annotate(period=models.functions.TruncDay('date'))
        elif filter_period == 'weekly':
            return queryset.annotate(period=models.functions.TruncWeek('date'))
        elif filter_period == 'monthly':
            return queryset.annotate(period=models.functions.TruncMonth('date'))
        elif filter_period == 'yearly':
            return queryset.annotate(period=models.functions.TruncYear('date'))
        return queryset

    def _get_total_sales_for_all_partners(self):
        """Get total sales for all partners."""
        return BimaErpSaleDocument.objects.all().aggregate(total_sales=models.Sum('total_amount'))['total_sales']
