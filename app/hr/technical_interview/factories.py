import factory
from factory import SubFactory
from .models import BimaHrTechnicalInterview, BimaHrEmployeeinterviewer
from hr.candidat.factories import BimaHrCandidatFactory
from hr.vacancie.factories import BimaHrVacancieFactory
from hr.interview_step.factories import BimaHrInterviewStepFactory
from hr.employee.factories import BimaHrEmployeeFactory
from common.enums.interview import get_interview_status_choices, get_interview_mode_choices

class BimaHrTechnicalInterviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrTechnicalInterview

    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('text')
    start_datetime = factory.Faker('date_time_between', start_date='-1d', end_date='+5d')
    end_datetime = factory.Faker('date_time_between', start_date='+6d', end_date='+10d')
    interview_mode = factory.Faker('random_element', elements=get_interview_mode_choices())
    location = factory.Faker('address')
    status = factory.Faker('random_element', elements=get_interview_status_choices())
    candidat = SubFactory(BimaHrCandidatFactory)
    vacancie = SubFactory(BimaHrVacancieFactory)
    interview_step = SubFactory(BimaHrInterviewStepFactory)
    link_interview = factory.Faker('url')
    id_event = factory.Faker('uuid4')

    @factory.post_generation
    def interviewers(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for interviewer in extracted:
            BimaHrEmployeeinterviewer.objects.create(employee=interviewer, technical_interview=self)

class BimaHrEmployeeinterviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrEmployeeinterviewer

    employee = SubFactory(BimaHrEmployeeFactory)
    technical_interview = SubFactory(BimaHrTechnicalInterviewFactory)
