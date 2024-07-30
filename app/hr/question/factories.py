import factory
from .models import BimaHrQuestion
from hr.question_category.factories import BimaHrQuestionCategoryFactory


class BimaHrQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrQuestion

    question = factory.Faker('word')
    question_category = factory.SubFactory(BimaHrQuestionCategoryFactory)
    active = factory.Faker('boolean')
