import factory
from .models import BimaHrInterviewStep
from common.enums.interview import get_interview_type_choices


class BimaHrInterviewStepFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrInterviewStep

    name = factory.Faker('word')
    interview_type = factory.Iterator(get_interview_type_choices())
    description= factory.Faker('text')
    active = factory.Faker('boolean')
