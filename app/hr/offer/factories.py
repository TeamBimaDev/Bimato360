import factory 
from.models import BimaHrOffre 
from hr.vacancie.factories import BimaHrVacancieFactory
from common.enums.position import get_seniority_choices, get_tone_choices

class BimaHrOfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrOffre

    title = factory.SubFactory(BimaHrVacancieFactory)
    work_location = factory.Faker('city')
    description = factory.Faker('text')
    seniority = factory.Iterator(get_seniority_choices())
    tone = factory.Iterator(get_tone_choices())
    salary = factory.Faker('pydecimal', left_digits=6, right_digits=3, positive= True)
    inclusive_emojis = factory.Faker('boolean')
    include_desc = factory.Faker('boolean')
    inclusive_education = factory.Faker('word')
    inclusive_contact = factory.Faker('word')
    inclusive_location = factory.Faker('boolean')
    inclusive_experience = factory.Faker('boolean')
    generated_content = factory.Faker('text')
