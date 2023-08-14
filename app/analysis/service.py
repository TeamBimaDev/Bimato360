import logging
from calendar import monthrange
from collections import defaultdict, OrderedDict
from datetime import date

from common.enums.partner_type import PartnerType
from django.db import models
from django.db.models import Sum, Count, Avg, DateField, Subquery, Case, When, Value, CharField, F
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear, Trunc, Concat
from django.shortcuts import get_object_or_404
from erp.product.models import BimaErpProduct
from erp.sale_document.models import BimaErpSaleDocument
from erp.sale_document.models import BimaErpSaleDocumentProduct

logger = logging.getLogger(__name__)


class BimaAnalysisService:

    @staticmethod
    def filter_sales_by_period(queryset, filter_period):
        if filter_period == 'daily':
            return queryset.annotate(period=models.functions.TruncDay('date')), models.functions.TruncDay('date')
        elif filter_period == 'weekly':
            return queryset.annotate(period=models.functions.TruncWeek('date')), models.functions.TruncWeek('date')
        elif filter_period == 'yearly':
            return queryset.annotate(period=models.functions.TruncYear('date')), models.functions.TruncYear('date')
        else:
            return queryset.annotate(period=models.functions.TruncMonth('date')), models.functions.TruncMonth('date')

    @staticmethod
    def filter_sales_product_by_period(queryset, filter_period):
        if filter_period == 'daily':
            return queryset.annotate(
                period=models.functions.TruncDay('date')), models.functions.TruncDay(
                'sale_document__date')
        elif filter_period == 'weekly':
            return queryset.annotate(
                period=models.functions.TruncWeek('date')), models.functions.TruncWeek(
                'sale_document__date')
        elif filter_period == 'yearly':
            return queryset.annotate(
                period=models.functions.TruncYear('date')), models.functions.TruncYear(
                'sale_document__date')
        else:
            return queryset.annotate(
                period=models.functions.TruncMonth('date')), models.functions.TruncMonth(
                'sale_document__date')

    @staticmethod
    def aggregate_sales_data(queryset):
        return queryset.values('period').annotate(
            total_sales=Sum('total_amount'),
            transaction_count=Count('id'),
            avg_transaction_value=Avg('total_amount')
        ).order_by('period')

    @staticmethod
    def calculate_partner_data(aggregated_data, partner_sales, all_sales):
        for data in aggregated_data:
            period = data['period']

            period_sales_for_partner = partner_sales.filter(period=period).aggregate(total_sales=Sum('total_amount'))[
                'total_sales']
            period_transaction_for_partner = partner_sales.filter(period=period).count()

            period_total_sales = all_sales.filter(period=period).aggregate(total_sales=Sum('total_amount'))[
                'total_sales']
            period_total_transactions = all_sales.filter(period=period).count()

            data['partner_percentage'] = BimaAnalysisService._percentage(period_sales_for_partner, period_total_sales)
            data['transaction_percentage_for_partner'] = BimaAnalysisService._percentage(period_transaction_for_partner,
                                                                                         period_total_transactions)

    @staticmethod
    def _percentage(part, whole):
        return round((part / whole) * 100, 2) if whole else 0.0

    @staticmethod
    def get_most_sold_products_data(sales_documents, filter_period, top_n):
        filtered_sales_documents, trunc_date = BimaAnalysisService.filter_sales_product_by_period(sales_documents,
                                                                                                  filter_period)

        products_data = BimaErpSaleDocumentProduct.objects.filter(sale_document__in=filtered_sales_documents) \
            .annotate(period=trunc_date) \
            .values('period', 'product__public_id', 'product__reference', 'product__name') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('period', '-total_sold')

        return BimaAnalysisService._format_top_n_products(products_data, top_n)

    @staticmethod
    def _format_top_n_products(products_data, top_n):
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
        return formatted_result

    @staticmethod
    def get_product_count_aggregated_sales(product_public_id, period):
        product = get_object_or_404(BimaErpProduct, public_id=product_public_id)
        period_mapping = {
            "daily": "day",
            "weekly": "week",
            "monthly": "month",
            "yearly": "year"
        }

        trunc_type = period_mapping.get(period, "day")  # Default to daily if the period is not recognized

        trunc_date = Trunc('sale_document__date', trunc_type, output_field=DateField())

        sales = (
            BimaErpSaleDocumentProduct.objects
            .filter(product_id=product.id)
            .annotate(period=trunc_date)
            .values('period')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('period')
        )

        results = []
        for sale in sales:
            if period == "daily":
                format_str = '%d/%m/%Y'
            elif period == "yearly":
                format_str = '%Y'
            elif period == "weekly":
                format_str = 'Week starting %d/%m/%Y'
            else:  # monthly
                format_str = '%m/%Y'

            results.append({
                "period": sale["period"].strftime(format_str),
                "quantity": sale["total_quantity"]
            })

        return results

    @staticmethod
    def get_unsold_products(self, start_date=None, end_date=None):
        sale_document_query = BimaErpSaleDocument.objects.all()
        if start_date:
            sale_document_query = sale_document_query.filter(date__gte=start_date)
        if end_date:
            sale_document_query = sale_document_query.filter(date__lte=end_date)

        sold_products = BimaErpSaleDocumentProduct.objects.filter(
            sale_document__in=sale_document_query
        ).values('product_id')

        return BimaErpProduct.objects.exclude(
            id__in=Subquery(sold_products)
        ).values('name', 'reference')

    @staticmethod
    def _get_trunc_mapper(period):
        return {
            'daily': TruncDay,
            'weekly': TruncWeek,
            'monthly': TruncMonth,
            'yearly': TruncYear
        }.get(period)

    @classmethod
    def get_aggregated_sales(cls, period, partner_id=None):
        trunc_function = cls._get_trunc_mapper(period)
        if not trunc_function:
            raise ValueError("Invalid period provided.")

        sales = BimaErpSaleDocument.objects.all()

        if partner_id:
            sales = sales.filter(partner_id=partner_id)

        sales = (sales
                 .annotate(period=trunc_function('date'))
                 .values('period')
                 .annotate(total=Sum('total_amount'))
                 .order_by('period'))
        return sales

    @staticmethod
    def calculate_percentage_difference(sales):
        result = []
        for i in range(1, len(sales)):
            try:
                previous_value = sales[i - 1]['total'] or 0
                current_value = sales[i]['total'] or 0

                difference = current_value - previous_value

                if previous_value != 0:
                    percentage_difference = (difference / previous_value) * 100
                else:

                    percentage_difference = 100 if current_value != 0 else 0

                result.append({
                    'period': sales[i]['period'],
                    'value': "{:.2f}%".format(percentage_difference)
                })
            except Exception as ex:
                logger.error(
                    f"Error occurred when calculate_percentage_difference previous_value: {previous_value}  "
                    f"current_value:{current_value}  with message {ex.args}")

        return result

    @staticmethod
    def annotate_partner_name(queryset):
        return queryset.annotate(
            partner_name=Case(
                When(partner__partner_type=PartnerType.INDIVIDUAL.name,
                     then=Concat(F('partner__first_name'), Value(' '), F('partner__last_name'))
                     ),
                default=F('partner__company_name'),
                output_field=CharField(),
            )
        )

    @staticmethod
    def get_top_partners(period='monthly', top_n=3, year=None, show_all_periods=False):
        trunc_map = {
            'daily': TruncDay,
            'weekly': TruncWeek,
            'monthly': TruncMonth,
            'yearly': TruncYear
        }

        sales = BimaErpSaleDocument.objects.annotate(period=trunc_map[period]('date'))

        if year:
            sales = sales.filter(date__year=year)

        data = (BimaAnalysisService.annotate_partner_name(sales)
                .values('period', 'partner_name')
                .annotate(total_amount=Sum('total_amount'))
                .order_by('period', '-total_amount'))

        grouped_data = OrderedDict()
        for item in data:
            period_str = item['period'].strftime('%Y-%m-%d') if isinstance(item['period'], date) else str(
                item['period'])

            if item['total_amount'] == 0:
                continue

            if period_str not in grouped_data:
                grouped_data[period_str] = []

            if len(grouped_data[period_str]) < top_n:
                grouped_data[period_str].append({
                    'name': item['partner_name'],
                    'total': item['total_amount']
                })

        # If show_all_periods is True, fill in the gaps.
        if show_all_periods and year:
            if period == 'monthly':
                for month in range(1, 13):
                    month_str = f"{year}-{month:02}-01"
                    if month_str not in grouped_data:
                        grouped_data[month_str] = []

            elif period == 'daily':
                for day in range(1, monthrange(year, 12)[1] + 1):
                    day_str = f"{year}-12-{day:02}"
                    if day_str not in grouped_data:
                        grouped_data[day_str] = []

            elif period == 'weekly':
                for week in range(1, 53):
                    week_start = f"{year}-W{week}-1"
                    if week_start not in grouped_data:
                        grouped_data[week_start] = []

        sorted_grouped_data = OrderedDict(sorted(grouped_data.items(), key=lambda x: x[0]))

        # Ensure each period has top_n items
        for key in sorted_grouped_data:
            while len(sorted_grouped_data[key]) < top_n:
                sorted_grouped_data[key].append({
                    'name': "",
                    'total': 0
                })

        # Change format
        formatted_data = []
        for key, value in sorted_grouped_data.items():
            formatted_data.append({
                'period': key,
                'partners': value
            })

        return {'partners': formatted_data}
