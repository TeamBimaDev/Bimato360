from factory import SubFactory
from .models import BimaHrInterview
from hr.vacancie.factories import BimaHrVacancieFactory
from hr.candidat.factories import BimaHrCandidatFactory
from hr.interview_step.factories import BimaHrInterviewStepFactory
import factory
from common.enums.interview import get_interview_status_choices, get_interview_due_data_choices, get_interview_time_choices

class BimaHrInterviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrInterview

    name = factory.Faker('word')
    due_date = factory.Faker('random_element', elements=get_interview_due_data_choices())
    scheduled_date = factory.Faker('date_between', start_date='-7d', end_date='today')
    status = factory.Faker('random_element', elements=get_interview_status_choices())
    candidat = SubFactory(BimaHrCandidatFactory)
    vacancie = SubFactory(BimaHrVacancieFactory)
    link_interview = factory.Faker('url')
    estimated_time = factory.Faker('random_element', elements=get_interview_time_choices())
    interview_step = SubFactory(BimaHrInterviewStepFactory)
    comments = factory.Faker('text')

    @classmethod
    def _generate(cls, strategy, attrs=None):
        attrs = attrs or {}
        if 'scheduled_date' in attrs:
            attrs['scheduled_date'] = cls._get_faker().date_between(start_date='-7d', end_date='today')
        return super()._generate(strategy, attrs)
