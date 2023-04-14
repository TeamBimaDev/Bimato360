from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import SkillCategory
from .serializers import BimaCoreSkillCategorySerializer


class MyModelTestCase(APITestCase):
    client = APIClient()

    @staticmethod
    def create_my_model(name):
        if name != "":
            SkillCategory.objects.create(name=name)

    def setUp(self):
        self.create_my_model("Test1")
        self.create_my_model("Test2")
        self.create_my_model("Test3")

    def test_get_all_my_models(self):
        """
        Test to get all MyModels.
        """
        response = self.client.get(
            reverse('hr:skillcategory-list')
        )
        expected = SkillCategory.objects.all()
        serialized = BimaCoreSkillCategorySerializer(expected, many=True)
        #self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_my_model(self):
        """
        Test to create a new MyModel.
        """
        data = {"name": "Test4"}
        response = self.client.post(
            reverse('hr:skillcategory-list'),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SkillCategory.objects.count(), 4)

    def test_get_single_my_model(self):
        """
        Test to get a single MyModel.
        """
        model = SkillCategory.objects.first()
        response = self.client.get(
            reverse('hr:skillcategory-detail', kwargs={"pk": model.id})
        )
        expected = BimaCoreSkillCategorySerializer(model)
        self.assertEqual(response.data, expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_model(self):

        """
        Test to update a MyModel.
        """
        model = SkillCategory.objects.first()
        data = {"name": "Test1_updated"}
        print(data)
        response = self.client.put(
            reverse('hr:skillcategory-detail', kwargs={"pk": model.id}),
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SkillCategory.objects.get(pk=model.id).name, "Test1_updated")


    def test_delete_my_model(self):
        """
        Test to delete a MyModel.
        """
        model = SkillCategory.objects.first()
        response = self.client.delete(
            reverse('hr:skillcategory-detail', kwargs={"pk": model.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SkillCategory.objects.count(), 2)