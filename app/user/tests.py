from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import User


class BimaUserTest(APITestCase):
    def setUp(self):
        self.create_permissions()
        self.client = APIClient()
        self.user_data = {
            "name": "my-test-user",
            "email": "user@gmail.com",
            "password": "12345",
            "confirm_password": "12345",
        }

    def test_create_user(self):
        url = reverse("user:user-list")
        response = self.client.post(url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["name"], self.user_data["name"])

    def create_permissions(self):
        permission_list = [
            ("user.user.can_create", "Can create user"),
        ]

        for permission_code, permission_name in permission_list:
            content_type = ContentType.objects.get_for_model(User)
            Permission.objects.get_or_create(
                codename=permission_code,
                name=permission_name,
                content_type=content_type,
            )
