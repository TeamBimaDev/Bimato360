import factory
from .models import BimaHrEmployee
from common.enums.employee_enum import (
    get_employment_type_choices,
    get_work_mode_choices,
    get_job_type_choices,
    get_employee_status_choices,
)

from hr.position.factories import BimaHrPositionFactory
from user.factories import UserFactory


class BimaHrEmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrEmployee

    employment_type = factory.Faker('random_element', elements=[choice[0] for choice in get_employment_type_choices()])
    work_mode = factory.Faker('random_element', elements=[choice[0] for choice in get_work_mode_choices()])
    job_type = factory.Faker('random_element', elements=[choice[0] for choice in get_job_type_choices()])
    employment_status = factory.Faker('random_element', elements=[choice[0] for choice in get_employee_status_choices()])
    probation_end_date = factory.Faker('date_between', start_date='-30d', end_date='+30d')
    last_performance_review = factory.Faker('date_between', start_date='-365d', end_date='-30d')
    salary = factory.Faker('pydecimal', left_digits=6, right_digits=3, positive=True)
    position = factory.SubFactory(BimaHrPositionFactory)
    balance_vacation = factory.Faker('random_int', min=0, max=30)
    virtual_balance_vacation = factory.Faker('random_int', min=0, max=30)
    user = factory.SubFactory(UserFactory)
