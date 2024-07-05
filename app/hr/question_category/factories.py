import factory
from .models import BimaHrQuestionCategory


class BimaHrQuestionCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrQuestionCategory

    name = factory.Faker('word')
    description = factory.Faker('text')
    active = factory.Faker('boolean')
    category = None
