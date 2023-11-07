from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from ...models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """
        ユーザの作成
        """
        request_data = {
            "username": "user001",
            "first_name": "太郎",
            "last_name": "田中",
            "password": "password",
            "email": "user001@sample.com",
            "age": 30,
            "description": "すごい人",
        }
        url = "/signup/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user001 = User.objects.get(username=request_data["username"])
        created_data = {**vars(user001)}

        test_target_params = [
            "username",
            "first_name",
            "last_name",
            "email",
            "age",
            "description",
        ]
        for param in test_target_params:
            self.assertEqual(created_data[param], request_data[param])

    def test_create_user_already_registered_username(self):
        """
        ユーザの作成、すでにユーザ名が登録されている
        """
        request_data = {
            "username": "user001",
            "first_name": "太郎",
            "last_name": "田中",
            "password": "password",
            "email": "user001@sample.com",
            "description": "すごい人",
        }
        url = "/signup/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data = {
            "username": "user001",
            "first_name": "二郎",
            "last_name": "鈴木",
            "password": "password",
            "email": "user002@sample.com",
            "description": "超すごい人",
        }
        url = "/signup/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
