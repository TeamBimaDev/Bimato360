from django.contrib.contenttypes.models import ContentType
import factory
from .models import BimaCoreEntityTag
from core.tag.factories import BimaCoreTagFactory

class BimaCoreEntityTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaCoreEntityTag
    tag = factory.SubFactory(BimaCoreTagFactory)
    id_manager = factory.Faker('pyint', min_value=0, max_value=9999)
    order = factory.Faker('pyint', min_value=1, max_value=100, step=1)
    parent_type = None
    parent_id = None
    content_object = None

    @classmethod
    def with_parent(cls, parent):
        return cls(parent_type=ContentType.objects.get_for_model(parent), parent_id=parent.id)
