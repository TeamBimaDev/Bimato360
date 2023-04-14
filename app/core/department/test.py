from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import BimaCoreDepartment
from .serializers import BimaCoreDepartmentSerializer


class MyModelTestCase(APITestCase):
    client = APIClient()

    @staticmethod
    def create_my_model(name):
        if name != "":

            BimaCoreDepartment.objects.create(name=name)

    def setUp(self):
        self.create_my_model("Test1")
        self.create_my_model("Test2")
        self.create_my_model("Test3")

    def test_get_all_my_models(self):
        """
        Test to get all MyModels.
        """
        response = self.client.get(
            reverse('core:bimacoredepartment-list')
        )
        expected = BimaCoreDepartment.objects.all()
        serialized = BimaCoreDepartmentSerializer(expected, many=True)
        print(response.data)
        print(serialized.data)

        #self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_my_model(self):
        """
        Test to create a new MyModel.
        """
        data = {"name": "ismail", "description": "test", "manager_id": 2}
        response = self.client.post(
            reverse('core:bimacoredepartment-list'),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(BimaCoreDepartment.objects.count(), 4)

    def test_get_single_my_model(self):
        """
        Test to get a single MyModel.
        """
        model = BimaCoreDepartment.objects.first()
        response = self.client.get(
            reverse('core:bimacoredepartment-detail', kwargs={"pk": model.id})
        )
        expected = BimaCoreDepartmentSerializer(model)
        self.assertEqual(response.data, expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_model(self):

        """
        Test to update a MyModel.
        """
        model = BimaCoreDepartment.objects.first()
        data = {"name": "ismail", "description": "test","manager_id": 2}

        response = self.client.put(
            reverse('core:bimacoredepartment-detail', kwargs={"pk": model.id}),
            data=data,
            format="json"
        )
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCoreDepartment.objects.get(pk=model.id).name, "ismail")


    def test_delete_my_model(self):
        """
        Test to delete a MyModel.
        """
        model = BimaCoreDepartment.objects.first()
        response = self.client.delete(
            reverse('core:bimacoredepartment-detail', kwargs={"pk": model.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #self.assertEqual(BimaCoreDepartment.objects.count(), 2)