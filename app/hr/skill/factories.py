import factory
from .models import BimaHrSkill
from hr.skill_category.factories import BimaHrSkillCategoryFactory


class BimaHrSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrSkill

    name = factory.Faker('word')
    skill_category = factory.SubFactory(BimaHrSkillCategoryFactory)
    description = factory.Faker('text')
    active = factory.Faker('boolean')
