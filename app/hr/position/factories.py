import factory
from core.department.factories import BimaCoreDepartmentFactory
from .models import BimaHrPosition
from common.enums.position import get_seniority_choices
from hr.job_category.factories import BimaHrJobCategoryFactory
from hr.employee.factories import BimaHrEmployeeFactory


class BimaHrPositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BimaHrPosition

    title = factory.Faker('job')
    description = factory.Faker('text')
    work_location = factory.Faker('city')
    seniority = factory.Faker('random_element', elements=[choice[0] for choice in get_seniority_choices()])
    requirements = factory.Faker('text')
    responsibilities = factory.Faker('text')
    department = factory.SubFactory(BimaCoreDepartmentFactory)
    job_category = factory.SubFactory(BimaHrJobCategoryFactory)
    manager = factory.SubFactory(BimaHrEmployeeFactory)