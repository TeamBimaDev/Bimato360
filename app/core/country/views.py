from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.response import Response
from core.abstract.views import AbstractViewSet
from core.country.serializers import BimaCoreCountrySerializer
from core.state.serializers import BimaCoreStateSerializer
from reportlab.lib.pagesizes import letter

from common.helpers.GeneratePdf import GeneratePdf
from common.helpers.NumberedCanvas import NumberedCanvas
from common.helpers.PdfTable import PdfTable
from django.db import transaction
from .models import BimaCoreCountry
import csv
import requests

from core.state.models import BimaCoreState

from core.currency.models import BimaCoreCurrency


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.select_related('currency').all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'code', 'phone_code']

    def get_object(self):
        obj = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def get_state_by_country(self, request, public_id=None):
        country = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['public_id'])
        states = BimaCoreState.objects.filter(country=country)
        serializer = BimaCoreStateSerializer(states, many=True)
        return Response(serializer.data)

    def generate_pdf(self, request):
        model_name = 'BimaCoreCountry'
        fields = ['name', 'code', 'currency']
        response = create_response()
        pdf = NumberedCanvas(response, pagesize=letter)
        pdf_table = PdfTable(model_name, fields)
        generate_pdf = GeneratePdf(response, pdf, pdf_table)
        return generate_pdf.generate()

    @transaction.atomic
    @action(detail=False, methods=['get'], url_path='populate_database_from_csv')
    def populate_database_from_csv(self, request):
        errors = []

        # Delete all existing data
        print("Deleting all states...")
        BimaCoreState.objects.all().delete()
        print("Deleting all countries...")
        BimaCoreCountry.objects.all().delete()

        # Fetch and insert country data from CSV
        print("Reading countries from CSV...")
        self.process_csv(
            url='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/countries.csv',
            processor=self.insert_country,
            errors=errors
        )

        # Fetch and insert state data from CSV
        print("Reading states from CSV...")
        self.process_csv(
            url='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/states.csv',
            processor=self.insert_state,
            errors=errors
        )

        # Return the result
        if errors:
            return Response({"status": "End of script with errors", "errors": errors})
        else:
            return Response({"status": "No errors found"})

    def process_csv(self, url, processor, errors):
        try:
            response = requests.get(url)
            csv_content = response.content.decode('utf-8').splitlines()
            reader = csv.DictReader(csv_content)

            for row in reader:
                processor(row, errors)

        except Exception as e:
            errors.append(str(e))

    def insert_country(self, row, errors):
        try:
            print(f"Inserting country: {row['name']}...")
            currency = BimaCoreCurrency.objects.filter(currency_unit_label=row['currency']).first()
            if not currency:
                currency = BimaCoreCurrency.objects.first()

            BimaCoreCountry.objects.create(
                name=row['name'],
                code=row['iso2'],
                iso3=row['iso3'],
                iso2=row['iso2'],
                phone_code=row['phone_code'],
                capital=row['capital'],
                address_format='',
                vat_label='',
                zip_required=False,
                currency=currency
            )

        except Exception as e:
            errors.append(f"Error inserting country {row['name']}: {str(e)}")

    def insert_state(self, row, errors):
        try:
            print(f"Inserting state: {row['name']}...")
            country = BimaCoreCountry.objects.filter(iso2=row['country_code']).first()
            if not country:
                country = BimaCoreCountry.objects.first()

            BimaCoreState.objects.create(
                name=row['name'],
                code=row['state_code'],
                country=country
            )

        except Exception as e:
            errors.append(f"Error inserting state {row['name']}: {str(e)}")


def create_response():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="countries.pdf"'
    return response
