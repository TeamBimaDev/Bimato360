import factory
from .models import BimaCoreAddress
from core.state.factories import BimaCoreStateFactory
from core.country.factories import BimaCoreCountryFactory
from django.contrib.contenttypes.models import ContentType


class BimaCoreAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreAddress

    number = factory.Faker('word')
    street = factory.Faker('word')
    street2 = factory.Faker('word')
    zip = factory.Faker('word')
    city = factory.Faker('word')
    contact_name = factory.Faker('name')
    contact_phone = factory.Faker('word')
    contact_email = factory.Faker('email')
    can_send_bill = factory.Faker('boolean')
    can_deliver = factory.Faker('boolean')
    latitude = factory.Faker('word')
    longitude = factory.Faker('word')
    note = factory.Faker('word')
    parent_id = factory.Faker('random_int')
    parent_type = ContentType.objects.get
    state = factory.SubFactory(BimaCoreStateFactory)
    country = factory.SubFactory(BimaCoreCountryFactory)
