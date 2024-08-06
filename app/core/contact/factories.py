<<<<<<< HEAD
from django.contrib.contenttypes.models import ContentType
from .models import BimaCoreContact
from common.enums.gender import get_gender_choices
import factory

class BimaCoreContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreContact

    name = factory.Faker('name')
    position = factory.Faker('job')
    department = factory.Faker('company_suffix')
    email = factory.Faker('email')
    fax = factory.Faker('phone_number')
    mobile = factory.Faker('phone_number')
    phone = factory.Faker('phone_number')
    gender = factory.Faker('random_element', elements=get_gender_choices())
    parent_type = None
    parent_id = None
    content_object = None

    @classmethod
    def with_parent(cls, parent):
        return cls(parent_type=ContentType.objects.get_for_model(parent), parent_id=parent.id)
=======
from django.contrib.contenttypes.models import ContentType
from .models import BimaCoreContact
from common.enums.gender import get_gender_choices
import factory

class BimaCoreContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreContact

    name = factory.Faker('name')
    position = factory.Faker('job')
    department = factory.Faker('company_suffix')
    email = factory.Faker('email')
    fax = factory.Faker('phone_number')
    mobile = factory.Faker('phone_number')
    phone = factory.Faker('phone_number')
    gender = factory.Faker('random_element', elements=get_gender_choices())
    parent_type = factory.LazyAttribute(lambda obj: ContentType.objects.get_for_model(obj.content_object))
    parent_id = factory.SelfAttribute('content_object.id')
    content_object = None

    @classmethod
    def with_parent(cls, parent):
        return cls(content_object=parent)
>>>>>>> origin/ma-branch
