from collections import defaultdict
from datetime import datetime, timedelta

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Concat, TruncMonth, TruncWeek, TruncDay
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from erp.product.models import BimaErpProduct
from erp.sale_document.models import BimaErpSaleDocument
from erp.sale_document.models import BimaErpSaleDocumentProduct
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class BimaAnalysisViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path="total_sales_report")
    def total_sales_report(self, request):
        partner_public_id = request.query_params.get('partner_public_id', None)
        filter_period = request.query_params.get("filter_period", 'monthly').lower()

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

    @action(detail=False, methods=['get'], url_path="most_sold_products")
    def most_sold_products(self, request):
        filter_period = request.query_params.get("filter_period", 'monthly').lower()
        top_n = int(request.query_params.get("top_n", 5))
        year = request.query_params.get("year")

        sales_documents = BimaErpSaleDocument.objects.all()
        if year:
            sales_documents = sales_documents.filter(date__year=int(year))

        if filter_period == 'daily':
            trunc_date = models.functions.TruncDay('sale_document__date')
        elif filter_period == 'weekly':
            trunc_date = models.functions.TruncWeek('sale_document__date')
        elif filter_period == 'yearly':
            trunc_date = models.functions.TruncYear('sale_document__date')
        else:
            trunc_date = models.functions.TruncMonth('sale_document__date')

        products_data = BimaErpSaleDocumentProduct.objects.filter(sale_document__in=sales_documents) \
            .annotate(period=trunc_date) \
            .values('period', 'product__public_id', 'product__reference', 'product__name') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('period', '-total_sold')

        # Now let's format and filter the results to get the top N for each period
        result = defaultdict(list)
        for item in products_data:
            period = item['period']
            if len(result[period]) < top_n:
                result[period].append({
                    'product_public_id': item['product__public_id'],
                    'product_name': item['product__name'],
                    'product_reference': item['product__reference'],
                    'total_sold': item['total_sold']
                })

        formatted_result = [{"period": period, "products": products} for period, products in result.items()]

        return Response(formatted_result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="product_sales_count")
    def product_sales_count(self, request):
        # Retrieve the filter period and product from the request
        filter_period = request.query_params.get("filter_period", 'monthly').lower()
        product_public_id = request.query_params.get('product_public_id', None)

        if not product_public_id:
            return Response({"error": _("Please select a product")}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)

        # Depending on the filter_period, truncate date accordingly
        if filter_period == 'daily':
            trunc_func = TruncDay
            period_format = "%d/%m/%Y"
        elif filter_period == 'weekly':
            trunc_func = TruncWeek
            period_format = "Week %W/%Y"
        else:  # Default to monthly
            trunc_func = TruncMonth
            period_format = "%m/%Y"

        # Aggregate sale_documents based on filter period
        grouped_sales_docs = BimaErpSaleDocument.objects.annotate(period=trunc_func('date')).values('period').order_by(
            'period').distinct()

        result = []

        # For each period, get the sum of the product's quantity from sale_document_products
        for grouped_sale in grouped_sales_docs:
            current_date = grouped_sale['period']

            if filter_period == 'daily':
                start_date = end_date = current_date
            elif filter_period == 'weekly':
                # Assuming Monday is the first day of the week
                start_date = current_date - timedelta(days=current_date.weekday())  # Monday
                end_date = start_date + timedelta(days=6)  # Sunday
            else:  # monthly
                start_date = current_date.replace(day=1)
                next_month = current_date.replace(day=28) + timedelta(
                    days=4)  # will be somewhere in the next month for sure
                end_date = next_month - timedelta(days=next_month.day)

            sale_docs_in_period = BimaErpSaleDocument.objects.filter(date__range=(start_date, end_date))

            # Now get the sum of the product's quantity in this period
            product_qty_in_period = \
                BimaErpSaleDocumentProduct.objects.filter(sale_document__in=sale_docs_in_period,
                                                          product=product).aggregate(
                    total_qty=Sum('quantity'))['total_qty'] or 0

            formatted_date = current_date.strftime(period_format)
            result.append({"period": formatted_date, "quantity": product_qty_in_period})

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="unsold_products")
    def unsold_products(self, request):
        start_date = request.query_params.get("start_date", None)
        end_date = request.query_params.get("end_date", None)

        # Return an error if start_date or end_date is not provided
        if not (start_date and end_date):
            return Response({"error": "Both start_date and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert string dates to datetime.date objects
        try:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Expected 'YYYY-MM-DD'."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Filter the sales documents within the provided date range
        sales_documents = BimaErpSaleDocument.objects.filter(date__range=(start_date_obj, end_date_obj))
        sale_document_ids = sales_documents.values_list('id', flat=True)

        sold_product_ids = BimaErpSaleDocumentProduct.objects.filter(
            sale_document_id__in=sale_document_ids).values_list('product_id', flat=True).distinct()

        unsold_products = BimaErpProduct.objects.exclude(id__in=sold_product_ids)

        unsold_products_data = [
            {
                'id': product.public_id,
                'name': product.name,
                'reference': product.reference,
            }
            for product in unsold_products
        ]

        return Response(unsold_products_data)

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
