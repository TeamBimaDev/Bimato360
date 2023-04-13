from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import BimaHrCondidatPoste
from .serializers import BimaHrCondidatPosteSerializer


class MyModelTestCase(APITestCase):
    client = APIClient()


    @staticmethod
    def create_my_model(expected_salary,proposed_salary ,accepted_salary):
        if (expected_salary != "") and (proposed_salary != ""):
            BimaHrCondidatPoste.objects.create(expected_salary=expected_salary ,proposed_salary=proposed_salary ,accepted_salary=accepted_salary)

    def setUp(self):
        self.create_my_model(120, 100, 110)
        self.create_my_model(120, 100, 110)
        self.create_my_model(120, 100, 110)

    def test_get_all_my_models(self):
        """
        Test to get all MyModels.
        """
        response = self.client.get(
            reverse('hr:bimahrcondidatposte-list')
        )
        expected = BimaHrCondidatPoste.objects.all()
        serialized = BimaHrCondidatPosteSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_my_model(self):
        """
        Test to create a new MyModel.

        """
        data = {
            "expected_salary": 120.0,
            "proposed_salary": 102.0,
            "accepted_salary": 100.0,
            "date": "2023-04-13T12:15:32.898860Z",
            "id_candidat": [1],
            "id_poste": [1]
        }

        response = self.client.post(
            reverse('hr:bimahrcondidatposte-list'),
            data=data,
            format="json"
        )
        print(response )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaHrCondidatPoste.objects.count(), 4)

    def test_get_single_my_model(self):
        """
        Test to get a single MyModel.
        """
        model = BimaHrCondidatPoste.objects.first()
        response = self.client.get(
            reverse('hr:bimahrcondidatposte-detail', kwargs={"pk": model.id})
        )
        expected = BimaHrCondidatPosteSerializer(model)
        self.assertEqual(response.data, expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_model(self):

        """
        Test to update a MyModel.
        """
        model = BimaHrCondidatPoste.objects.first()
        data = {
            "expected_salary": 120.0,
            "proposed_salary": 102.0,
            "accepted_salary": 100.0,
            "date": "2023-04-13T12:15:32.898860Z",
            "id_candidat": [1],
            "id_poste": [1]
        }


        response = self.client.put(
            reverse('hr:bimahrcondidatposte-detail', kwargs={"pk": model.id}),
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrCondidatPoste.objects.get(pk=model.id).name, "Test1_updated")


    def test_delete_my_model(self):
        """
        Test to delete a MyModel.
        """
        model = BimaHrCondidatPoste.objects.first()
        response = self.client.delete(
            reverse('hr:bimahrcondidatposte-detail', kwargs={"pk": model.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BimaHrCondidatPoste.objects.count(), 2)