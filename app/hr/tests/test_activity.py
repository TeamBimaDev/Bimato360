
from django.test import TestCase
from hr.activity.models import BimaHrActivity
from core.abstract.models import AbstractModel
from hr.activity_type.models import BimaHrActivityType
from hr.applicant.models import BimaHrApplicant

class MyAbstractModelTestCase(TestCase):
    def test_my_concrete_model_string_method(self):
        activity_type = BimaHrActivityType.objects.create(name='dev', description='Test Description')
        applicant = BimaHrApplicant.objects.create(first_name='Test Applicant')
        my_concrete_model = BimaHrActivity.objects.create(
            name='Test Title',
            description='Test Description',
            start_date='2022-09-20',
            end_date='2022-09-20',
            id_manager=1,
            actvity_type=activity_type,
            applicant=applicant,
        )
        self.assertEqual(str(my_concrete_model), "('Test Title', 'Test Description', '2022-09-20 00:00:00+00', '2022-09-20 00:00:00+00', 1, None, 1)")