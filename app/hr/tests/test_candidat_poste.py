from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from hr.condidatposte.models import BimaHrCondidatPoste
from hr.condidatposte.serializers import BimaHrCondidatPosteSerializer


class MyModelTestCase(APITestCase):
    client = APIClient()

    @staticmethod
    def create_my_model(expected_salary):
        if expected_salary != "":
            t=BimaHrCondidatPoste.objects.create(expected_salary=expected_salary)
            print(t)


    def setUp(self):
        self.create_my_model(100)
        self.create_my_model(70)
        self.create_my_model(10)

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
        data = {
            "expected_salary": 100.0,
            "proposed_salary": 120.0,
            "accepted_salary": 110.0,
            "date": "2023-04-14T09:09:00.799582Z",
            "id_candidat": [],
            "id_poste": []
        }



        response = self.client.post(reverse('hr:bimahrcondidatposte-list'), data)

        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )

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

    def test_update_my_model(self ):

        """
        Test to update a MyModel.
        """
        model = BimaHrCondidatPoste.objects.first()
        data = {
            "expected_salary": 100.0,
            "proposed_salary": 120.0,
            "accepted_salary": 110.0,
            "date": "2023-04-14T09:09:00.799582Z",
            "id_candidat": [],
            "id_poste": []
        }





        response = self.client.put(
            reverse('hr:bimahrcondidatposte-detail', kwargs={"pk": model.id}),
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaHrCondidatPoste.objects.get(pk=model.id).expected_salary, 100)


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