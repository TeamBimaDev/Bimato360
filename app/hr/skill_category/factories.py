import factory
from .models import BimaHrSkillCategory


class BimaHrSkillCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrSkillCategory

    name = factory.Faker('word')
    description = factory.Faker('text')
    active = factory.Faker('boolean')
    category = None
