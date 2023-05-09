from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from core.poste.models import BimaCorePoste
from core.poste.serializers import BimaCorePostESerializer


class MyModelTestCase(APITestCase):
    client = APIClient()

    @staticmethod
    def create_my_model(name):
        if name != "":

            BimaCorePoste.objects.create(name=name)

    def setUp(self):
        self.create_my_model("Test1")
        self.create_my_model("Test2")
        self.create_my_model("Test3")

    def test_get_all_my_models(self):
        """
        Test to get all MyModels.
        """
        response = self.client.get(
            reverse('core:bimacoreposte-list')
        )
        expected = BimaCorePoste.objects.all()
        serialized = BimaCorePostESerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_my_model(self):
        """
        Test to create a new MyModel.
        """
        data= {"name": "museumar", "description": "vhqjna", "requirements": "nkcxAN", "responsabilités":"N%XN%ZAdxa"}
        response = self.client.post(
            reverse('core:bimacoreposte-list'),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BimaCorePoste.objects.count(), 4)

    def test_get_single_my_model(self):
        """
        Test to get a single MyModel.
        """
        model = BimaCorePoste.objects.first()
        response = self.client.get(
            reverse('core:bimacoreposte-detail', kwargs={"pk": model.id})
        )
        expected = BimaCorePostESerializer(model)
        self.assertEqual(response.data, expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_my_model(self):

        """
        Test to update a MyModel.
        """
        model = BimaCorePoste.objects.first()
        data = {"name": "museumar", "description": "vhqjna", "requirements": "nkcxAN", "responsabilités": "N%XN%ZAdxa"}

        response = self.client.put(
            reverse('core:bimacoreposte-detail', kwargs={"pk": model.id}),
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BimaCorePoste.objects.get(pk=model.id).name, "ismail")


    def test_delete_my_model(self):
        """
        Test to delete a MyModel.
        """
        model = BimaCorePoste.objects.first()
        response = self.client.delete(
            reverse('core:bimacoreposte-detail', kwargs={"pk": model.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(BimaCorePoste.objects.count(), 2)