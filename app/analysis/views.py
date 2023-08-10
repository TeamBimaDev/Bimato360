from django.shortcuts import get_object_or_404
from erp.partner.models import BimaErpPartner
from erp.sale_document.models import BimaErpSaleDocument
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .service import BimaAnalysisService


class BimaAnalysisViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path="total_sales_report")
    def total_sales_report(self, request):
        partner_public_id = request.query_params.get('partner_public_id', None)
        filter_period = request.query_params.get("filter_period", 'monthly').lower()

        all_sales, trunc_date = BimaAnalysisService.filter_sales_by_period(BimaErpSaleDocument.objects.all(),
                                                                           filter_period)

        if partner_public_id:
            partner = get_object_or_404(BimaErpPartner, public_id=partner_public_id)
            sales_for_partner = all_sales.filter(partner__id=partner.id)
        else:
            sales_for_partner = all_sales

        aggregated_data = BimaAnalysisService.aggregate_sales_data(sales_for_partner)

        if partner_public_id:
            BimaAnalysisService.calculate_partner_data(aggregated_data, sales_for_partner, all_sales)

        return Response({'aggregated_data': aggregated_data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="most_sold_products")
    def most_sold_products(self, request):
        filter_period = request.query_params.get("filter_period", 'monthly').lower()
        top_n = int(request.query_params.get("top_n", 10))

        sales_data = BimaErpSaleDocument.objects.all()
        result = BimaAnalysisService.get_most_sold_products_data(sales_data, filter_period, top_n)

        return Response({'products': result}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="product_sales_count")
    def product_sales_count(self, request):
        product_public_id = self.request.query_params.get('product_public_id', None)
        filter_period = self.request.query_params.get('period', 'monthly').lower()

        if not product_public_id:
            return Response({"error": "product_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        results = BimaAnalysisService.get_product_count_aggregated_sales(product_public_id, filter_period)

        return Response(results, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="unsold_products")
    def unsold_products(self, request):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        unsold_products = BimaAnalysisService.get_unsold_products(start_date, end_date)

        result = [
            {
                "product_name": product['name'],
                "product_reference": product['reference'],
                "date_range": f"{start_date or 'beginning'} to {end_date or 'now'}"
            }
            for product in unsold_products
        ]

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path="sales_income_evolution_percentage")
    def sales_income_evolution_percentage(self, request):
        period = request.query_params.get('filter_period', 'monthly').lower()

        try:
            aggregated_sales = BimaAnalysisService.get_aggregated_sales(period)
            report = BimaAnalysisService.calculate_percentage_difference(aggregated_sales)
            return Response(report)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=500)
