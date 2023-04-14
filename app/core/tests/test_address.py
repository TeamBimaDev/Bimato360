from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.currency.models import BimaCoreCurrency
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState

from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer

class BimaCoreAddressCreateTestCase(TestCase):
    currency = {}
    country = {}
    state = {}
    contentType = {}
    def setUp(self):
        client = APIClient()
        self.currency_data = {
            'name': 'EURO',
            'symbol': 'E',
            'rounding': 3456,
            'decimal_places': 5678,
            'active': True,
            'position': 'FFF',
            'currency_unit_label': 'EEE111',
            'currency_subunit_label': 'RRR111',
        }

        self.country_data = {
            'name': 'France',
            'code': '480',
            'address_format': 'paris',
            'address_view_id': 12,
            'phone_code': 480,
            "name_position": "BB",
            'vat_label': 'FF',
            'state_required': True,
            'zip_required': True,
            'currency_id': 1,
        }

        self.state_data = {
            'name': 'paris',
            'code': '480',
            'country_id': 1,
        }
        global currency
        global country
        global state
        global contentType
        currency = BimaCoreCurrency.objects.create(**self.currency_data)
        country = BimaCoreCountry.objects.create(**self.country_data)
        state = BimaCoreState.objects.create(**self.state_data)
        contentType = ContentType.objects.filter(app_label="core", model="bimacoreaddress").first()
        self.address_data = {
            "number": "1",
            "street": "Rue ibn khouldoun",
            "street2": "Rue ibn Jazzar",
            "zip": "3113",
            "city": "Kairouan",
            "parent_type": contentType.pk,
            "country": country.pk,
            "parent_id": 1,
            "state": state.pk,
        }
    def test_create_address(self):
        url_create = reverse('core:bimacoreaddress-list')
        response = self.client.post(url_create, data=self.address_data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCoreAddress.objects.count(), 1)
        self.assertEqual(BimaCoreAddress.objects.get().number, self.address_data['number'])
        self.assertEqual(BimaCoreAddress.objects.get().street, self.address_data['street'])
        self.assertEqual(BimaCoreAddress.objects.get().street2, self.address_data['street2'])
        self.assertEqual(BimaCoreAddress.objects.get().zip, self.address_data['zip'])
        self.assertEqual(BimaCoreAddress.objects.get().city, self.address_data['city'])
        self.assertEqual(BimaCoreAddress.objects.get().state.pk, self.address_data['state'])
        self.assertEqual(BimaCoreAddress.objects.get().country.pk, self.address_data['country'])
