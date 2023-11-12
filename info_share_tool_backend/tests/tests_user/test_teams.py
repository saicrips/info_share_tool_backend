from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from ...models import User, Team, TeamAdministrator, TeamMember


class TeamTestCase(TestCase):
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

    def setUp(self):
        self.client = APIClient()

    def test_create_team(self):
        """
        チームを作成する
        """

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
        response = self.client.post(url, request_data, format="json")
        # print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # テスト対象パラメタ
        test_target_params = [
            "name",
            "description",
            "administrators",
            "members",
        ]
        for param in test_target_params:
            if isinstance(request_data[param], list):
                self.assertEqual(set(response.data[param]), set(request_data[param]))
            else:
                self.assertEqual(response.data[param], request_data[param])

    def test_create_team_no_creator(self):
        """
        チームを作成する 管理者に作成者が存在しない
        """

        request_data = {
            "name": "チーム",
            "description": "最初のチーム",
            "operator_user": "user001",
            "administrators": ["user002", "user003"],
            "members": [
                "user004",
                "user005",
                "user006",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")

        request_data["administrators"].append(request_data["operator_user"])

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # テスト対象パラメタ
        test_target_params = [
            "name",
            "description",
            "administrators",
            "members",
        ]
        for param in test_target_params:
            if isinstance(request_data[param], list):
                self.assertEqual(set(response.data[param]), set(request_data[param]))
            else:
                self.assertEqual(response.data[param], request_data[param])

    def test_create_team_no_user(self):
        """
        チームを作成する
        存在しないメンバーの登録
        """

        request_data = {
            "name": "チーム",
            "description": "最初のチーム",
            "operator_user": "user001",
            "administrators": ["user0i1", "user002"],
            "members": [
                "user0i3",
                "user0i4",
                "user005",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_team(self):
        """
        チームを更新する
        """

        request_data = {
            "name": "チームA",
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
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data = {
            "name": "チームB",
            "description": "更新されたチーム",
            "operator_user": "user001",
            "administrators": ["user003", "user004"],
            "members": [
                "user006",
                "user007",
                "user008",
            ],
        }

        team_id = response.data.get("id")
        url = f"/team/{team_id}"
        response = self.client.put(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data["administrators"].append(request_data["operator_user"])

        # テスト対象パラメタ
        test_target_params = [
            "name",
            "description",
            "administrators",
            "members",
        ]
        for param in test_target_params:
            if isinstance(request_data[param], list):
                self.assertEqual(set(response.data[param]), set(request_data[param]))
            else:
                self.assertEqual(response.data[param], request_data[param])

    def test_update_team_no_permission(self):
        """
        権限のないチームを更新する
        """

        request_data = {
            "name": "チームA",
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
        response = self.client.post(url, request_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data = {
            "name": "チームB",
            "description": "更新されたチーム",
            "operator_user": "user003",
            "administrators": ["user001", "user002", "user003"],
            "members": [
                "user006",
                "user007",
                "user008",
            ],
        }

        team_id = response.data.get("id")
        url = f"/team/{team_id}"
        response = self.client.put(url, request_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_team(self):
        """
        チームを削除する
        """

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
        response = self.client.post(url, request_data, format="json")
        team_id = response.data.get("id")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data = {
            "operator_user": "user001",
        }
        url = f"/team/{team_id}"
        response = self.client.delete(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertRaises(Team.DoesNotExist, Team.objects.get, id=team_id)
        self.assertRaises(
            TeamAdministrator.DoesNotExist, TeamAdministrator.objects.get, id=team_id
        )
        self.assertRaises(TeamMember.DoesNotExist, TeamMember.objects.get, id=team_id)

    def test_delete_team_no_permission(self):
        """
        権限のないチームを削除する
        """

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
        response = self.client.post(url, request_data, format="json")
        team_id = response.data.get("id")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request_data = {
            "operator_user": "user003",
        }
        url = f"/team/{team_id}"
        response = self.client.delete(url, request_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_team(self):
        """
        チームを取得する
        """

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
        response = self.client.post(url, request_data, format="json")
        team_id = response.data.get("id")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        _request_data = {
            "operator_user": "user001",
        }
        url = f"/team/{team_id}"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # テスト対象パラメタ
        test_target_params = [
            "name",
            "description",
            "administrators",
            "members",
        ]
        for param in test_target_params:
            if isinstance(request_data[param], list):
                self.assertEqual(set(response.data[param]), set(request_data[param]))
            else:
                self.assertEqual(response.data[param], request_data[param])

    def test_get_team_not_found(self):
        """
        チームを取得する 存在しないチーム
        """

        all_team_ids = [team.team_id for team in Team.objects.all()]
        if len(all_team_ids) > 0:
            not_found_team_id = max(all_team_ids)
        else:
            not_found_team_id = 1

        _request_data = {
            "operator_user": "user001",
        }
        url = f"/team/{not_found_team_id}"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_team_no_permission(self):
        """
        権限のないチームを取得する
        """

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
        response = self.client.post(url, request_data, format="json")
        team_id = response.data.get("id")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        _request_data = {
            "operator_user": "user006",
        }
        url = f"/team/{team_id}"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
