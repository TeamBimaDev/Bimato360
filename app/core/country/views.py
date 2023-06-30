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


from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.select_related('currency').all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'code', 'phone_code']

    action_permissions = {
        'list': ['country.can_read'],
        'create': ['country.can_create'],
        'retrieve': ['country.can_read'],
        'update': ['country.can_update'],
        'partial_update': ['country.can_update'],
        'destroy': ['country.can_delete'],
    }

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
            processor=self.insert_countries,
            errors=errors
        )

        # Fetch and insert state data from CSV
        print("Reading states from CSV...")
        self.process_csv(
            url='https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/states.csv',
            processor=self.insert_states,
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

            processor(reader, errors)

        except Exception as e:
            errors.append(str(e))

    def insert_countries(self, reader, errors):
        country_list = []
        try:
            for row in reader:
                print(f"Preparing country: {row['name']} for insertion...")
                currency = BimaCoreCurrency.objects.filter(currency_unit_label=row['currency']).first()
                if not currency:
                    currency = BimaCoreCurrency.objects.first()

                country = BimaCoreCountry(
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
                country_list.append(country)

            print("Bulk inserting countries...")
            BimaCoreCountry.objects.bulk_create(country_list)

        except Exception as e:
            errors.append(f"Error preparing countries for bulk insertion: {str(e)}")

    def insert_states(self, reader, errors):
        state_list = []
        try:
            for row in reader:
                print(f"Preparing state: {row['name']} for insertion...")
                country = BimaCoreCountry.objects.filter(iso2=row['country_code']).first()
                if not country:
                    country = BimaCoreCountry.objects.first()

                state = BimaCoreState(
                    name=row['name'],
                    code=row['state_code'],
                    country=country
                )
                state_list.append(state)

            print("Bulk inserting states...")
            BimaCoreState.objects.bulk_create(state_list)

        except Exception as e:
            errors.append(f"Error preparing states for bulk insertion: {str(e)}")


def create_response():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="countries.pdf"'
    return response
