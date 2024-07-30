from factory import SubFactory
from .models import BimaHrInterviewQuestion
from hr.interview.factories import BimaHrInterviewFactory
import factory

class BimaHrInterviewQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrInterviewQuestion

    question = factory.Faker('text')
    response = factory.Faker('text', max_nb_chars=200)  
    interview = SubFactory(BimaHrInterviewFactory)
