from django.test import TestCase
from .models import BimaHrActivityType
from core.abstract.models import AbstractModel
class MyAbstractModelTestCase(TestCase):
   # def test_my_abstract_model_string_method(self):
    #    my_abstract_model = AbstractModel.objects.create()
     #   with self.assertRaises(NotImplementedError):
    #        str(my_abstract_model)

    def test_my_concrete_model_string_method(self):
        my_concrete_model = BimaHrActivityType.objects.create(name ="Test Title", description="Test Description")
        self.assertEqual(str(my_concrete_model), "('Test Title', 'Test Description')")


    def test_my_update_model_string_method(self):
        my_concrete_model = BimaHrActivityType.objects.create(name="Test Title", description="Test Description")
        BimaHrActivityType.objects.update(name="Test Title1", description="Test Description1")
        my_concrete_model = BimaHrActivityType.objects.get(pk=my_concrete_model.pk)
        self.assertEqual(str(my_concrete_model), "('Test Title1', 'Test Description1')")