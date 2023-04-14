from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import BimaHrSkill
from .serializers import BimaHrSkillSerializer
from hr.skill_category.models import SkillCategory


class MyModelTestCase(APITestCase):
    client = APIClient()
    data = {
        "name": "python",
        "skillcategorys_id": 1,
        "applicant": [
            1
        ]
    }

    @staticmethod
    def create_my_model(name):
        if name != "":
            category = SkillCategory.objects.create(name=name)
            BimaHrSkill.objects.create(name=name, skillcategorys=category )
    def setUp(self):
        self.create_my_model("Test1")
        self.create_my_model("Test2")
        self.create_my_model("Test3")

    def test_get_all_my_models(self):
        """
        Test to get all MyModels.
        """
        response = self.client.get(
            reverse('hr:bimahrskill-list')
        )
        expected = BimaHrSkill.objects.all()
        serialized = BimaHrSkillSerializer(expected, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_my_model(self):
        data = {
            "name": "python",
            "skillcategorys_id": 1,
            "applicant": []
        }

        response = self.client.post(reverse('hr:bimahrskill-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_my_model(self):
        """
        Test to get a single MyModel.
        """
        model = BimaHrSkill.objects.first()
        response = self.client.get(
            reverse('hr:bimahrskill-detail', kwargs={"pk": model.id})
        )
        expected = BimaHrSkillSerializer(model)
        self.assertEqual(response.data, expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_model(self ):

        """
        Test to update a MyModel.
        """
        model = BimaHrSkill.objects.first()
        data = {
           "id" : model.id,
            "name": "python test",
            "skillcategorys_id": 1,
        }

        response = self.client.put(
            reverse('hr:bimahrskill-detail', kwargs={"pk": model.id}),
            data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrSkill.objects.get(pk=model.id).name, "python test")


    def test_delete_my_model(self):
        """
        Test to delete a MyModel.
        """
        model = BimaHrSkill.objects.first()
        response = self.client.delete(
            reverse('hr:bimahrskill-detail', kwargs={"pk": model.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BimaHrSkill.objects.count(), 2)