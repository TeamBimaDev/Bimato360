from django.contrib.contenttypes.models import ContentType
from factory import Faker
from .models import BimaCoreAddress
from core.country.factories import BimaCoreCountryFactory
from core.state.factories import BimaCoreStateFactory
import factory

class BimaCoreAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreAddress

    number = Faker('building_number')
    street = Faker('street_name')
    street2 = Faker('secondary_address')
    zip = Faker('postcode')
    city = Faker('city')
    contact_name = Faker('name')
    contact_phone = Faker('phone_number')
    contact_email = Faker('email')
    can_send_bill = Faker('boolean')
    can_deliver = Faker('boolean')
    latitude = Faker('latitude')
    longitude = Faker('longitude')
    note = Faker('text')
    state = BimaCoreStateFactory()
    country = BimaCoreCountryFactory()
    parent_type = None
    parent_id = None
    content_object = None

    @classmethod
    def with_parent(cls, parent):
        return cls(parent_type=ContentType.objects.get_for_model(parent), parent_id=parent.id)
