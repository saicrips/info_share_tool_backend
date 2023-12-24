from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ...models import User, Team, TeamAdministrator, TeamMember
from ... import models


class ChannelTestCase(TestCase):
    @staticmethod
    def setUpTestData():
        users = []
        for i in range(0, 10):
            users.append(
                User(
                    username=f"user{str(i).zfill(3)}",
                    password="password",
                    first_name="田中",
                    last_name=f"{i}太郎",
                    email=f"user{str(i).zfill(3)}@sample.com",
                )
            )
        User.objects.bulk_create(users)

        client = APIClient()

        request_data = {
            "name": "チーム",
            "description": "最初のチーム",
            "operator_user": "user001",
            "administrators": ["user001", "user002"],
            "members": [
                "user003",
                "user004",
                "user005",
            ],
        }
        url = "/team/"
        response = client.post(url, request_data, format="json")
        ChannelTestCase.created_team_id = response.data["id"]

    def setUp(self):
        self.client = APIClient()

    def test_create_channel(self):
        """
        チャネルを作成する
        """

        request_data = {
            "name": "チャネル",
            "team": ChannelTestCase.created_team_id,
            "description": "最初のチャネル",
            "operator_user": "user001",
            "members": [
                "user003",
                "user004",
            ],
        }
        url = "/channel/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data["creator"] = request_data["operator_user"]
        # テスト対象パラメタ
        test_target_params = [
            "name",
            "description",
            "members",
            "creator",
        ]
        for param in test_target_params:
            if isinstance(request_data[param], list):
                self.assertEqual(set(response.data[param]), set(request_data[param]))
            else:
                self.assertEqual(response.data[param], request_data[param])

    def test_create_channel_no_team(self):
        """
        チャネルを作成する チームが存在しない
        """

        # 存在しないチームIDを取得
        teams: Team = Team.objects.all()
        team_ids = [team.id for team in teams]
        not_found_team_id = max(team_ids) + 1

        request_data = {
            "name": "チャネル",
            "team": not_found_team_id,
            "description": "最初のチャネル",
            "operator_user": "user001",
            "members": [
                "user003",
                "user004",
            ],
        }
        url = "/channel/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_channel_no_permission(self):
        """
        チャネルを作成する 作成する権限がない
        """

        request_data = {
            "name": "チャネル",
            "team": ChannelTestCase.created_team_id,
            "description": "最初のチャネル",
            "operator_user": "user006",
            "members_scope": 1,
            "members": [
                "user003",
                "user004",
            ],
        }
        url = "/channel/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_channel(self):
        """
        チャネルを更新する
        """

        request_data = {
            "name": "チャネル",
            "team": ChannelTestCase.created_team_id,
            "description": "最初のチャネル",
            "operator_user": "user001",
            "members": [
                "user003",
                "user004",
            ],
        }
        url = "/channel/"
        response = self.client.post(url, request_data, format="json")
        
        request_data = {
            "team": ChannelTestCase.created_team_id,
            "name": "チャネル",
            "description": "最初のチャネル",
            "operator_user": "user001",
            "members": [
                "user003",
                "user005",
            ],
        }
        
        channel_id = response.data.get("id")
        url = f"/channel/{channel_id}"
        response = self.client.put(url, request_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data["creator"] = request_data["operator_user"]
        # テスト対象パラメタ
        test_target_params = [
            "name",
            "description",
            "members",
            "creator",
        ]
        for param in test_target_params:
            if isinstance(request_data[param], list):
                self.assertEqual(set(response.data[param]), set(request_data[param]))
            else:
                self.assertEqual(response.data[param], request_data[param])