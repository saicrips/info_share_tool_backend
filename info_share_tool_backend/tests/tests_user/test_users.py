from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ...models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_user(self):
        """
        ユーザ名を指定してユーザ情報を取得する
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
        self.client.post(url, request_data, format="json")

        url = f"/user/{request_data['username']}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # テスト対象パラメタ
        test_target_params = [
            "username",
            "first_name",
            "last_name",
            "email",
            "age",
            "description",
        ]
        for param in test_target_params:
            self.assertEqual(response.data[param], request_data[param])

    def test_get_user_not_found(self):
        """
        存在しないユーザを指定する
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
        self.client.post(url, request_data, format="json")

        url = f"/user/user00i"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
