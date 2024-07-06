import factory
from.models import BimaHrVacancie, BimaHrCandidatVacancie
from core.department.factories import BimaCoreDepartmentFactory
from hr.job_category.factories import BimaHrJobCategoryFactory
from hr.employee.factories import BimaHrEmployeeFactory
from hr.candidat.factories import BimaHrCandidatFactory 
from common.enums.position import get_seniority_choices, get_position_status_choices
from common.enums.employee_enum import get_work_mode_choices, get_job_type_choices




class BimaHrVacancieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrVacancie

    title = factory.Faker("text", max_nb_chars=50)
    description = factory.Faker('text') 
    work_location = factory.Faker('city')
    seniority = factory.Iterator(get_seniority_choices())
    department = factory.SubFactory(BimaCoreDepartmentFactory)
    job_category = factory.SubFactory(BimaHrJobCategoryFactory)
    work_mode = factory.Iterator(get_work_mode_choices())
    job_type = factory.Iterator(get_job_type_choices())
    manager = factory.SubFactory(BimaHrEmployeeFactory)
    date_expiration = factory.Faker('date_this_year')
    date_start_vacancie = factory.Faker('date_this_year')
    number_of_positions = factory.Faker('pyint', min_value=1, max_value=10)
    position_status = factory.Iterator(get_position_status_choices())

class BimaHrCandidatVacancieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrCandidatVacancie

    candidat = factory.SubFactory(BimaHrCandidatFactory)
    vacancie = factory.SubFactory(BimaHrVacancieFactory)
    expected_salary = factory.Faker('pyfloat', left_digits=6, right_digits=2, positive=True)
    proposed_salary = factory.Faker('pyfloat', left_digits=6, right_digits=2, positive=True)
    accepted_salary = factory.Faker('pyfloat', left_digits=6, right_digits=2, positive=True)
    date = factory.Faker('date_time')
    comments = factory.Faker('sentence')
