import factory 
from.models import BimaHrOffre 
from hr.vacancie.factories import BimaHrVacancieFactory
<<<<<<< HEAD
from common.enums.position import get_seniority_choices, get_tone_choices, get_offre_status_choices
=======
from common.enums.position import get_seniority_choices, get_tone_choices
>>>>>>> origin/ma-branch

class BimaHrOfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrOffre

    title = factory.SubFactory(BimaHrVacancieFactory)
    work_location = factory.Faker('city')
    description = factory.Faker('text')
<<<<<<< HEAD
    seniority = factory.Faker('random_element', elements=[choice[0] for choice in get_seniority_choices()])
    tone = factory.Faker('random_element', elements=[choice[0] for choice in get_tone_choices()])
    salary = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    selected_hard_skills = factory.Faker('text')
    selected_soft_skills = factory.Faker('text')
    inclusive_emojis = factory.Faker('boolean')
    include_desc = factory.Faker('boolean')
    inclusive_education = factory.Faker('text', max_nb_chars=100)
    inclusive_contact = factory.Faker('text')
    inclusive_location = factory.Faker('boolean')
    inclusive_experience = factory.Faker('boolean')
    generated_content = factory.Faker('text')
    activated_at = factory.Faker('date_time', tzinfo=None)
    stopped_at = factory.Faker('date_between', start_date='-30d', end_date='+30d')
    status = factory.Faker('random_element', elements=[choice[0] for choice in get_offre_status_choices()])
=======
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
>>>>>>> origin/ma-branch
