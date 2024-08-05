from factory import lazy_attribute
import factory
from factory.django import DjangoModelFactory
from .models import BimaHrActivity
from hr.activity_type.factories import BimaHrActivityTypeFactory
from common.enums.activity_status import get_activity_status_choices
from hr.employee.factories import BimaHrEmployeeFactory
from datetime import timedelta


class BimaHrActivityFactory(DjangoModelFactory):
    class Meta:
        model = BimaHrActivity

    name = factory.Faker('name')
    description = factory.Faker('text')
    status = factory.Faker('random_element', elements=[choice[0] for choice in get_activity_status_choices()])
    start_date = factory.Faker('date_time')
    end_date = lazy_attribute(lambda obj: obj.start_date + timedelta(days=1))
    activity_type = factory.SubFactory(BimaHrActivityTypeFactory)
    organizer = factory.SubFactory(BimaHrEmployeeFactory)
