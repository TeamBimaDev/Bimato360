import factory
from .models import BimaHrCandidat



class BimaHrCandidatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrCandidat

    availability_days = factory.Faker('random_int', min=1, max=7)
    message = factory.Faker('text')
    
