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

        request_data = {
            "name": "チーム1",
            "description": "子丑寅卯辰巳午未申酉戌亥",
            "operator_user": "user001",
            "administrators": ["user001", "user002"],
            "members": [
                "user003",
                "user004",
                "user005",
                "user006",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")
        request_data = {
            "name": "チーム2",
            "description": "子丑寅卯辰巳",
            "operator_user": "user002",
            "administrators": ["user002", "user003"],
            "members": [
                "user004",
                "user005",
                "user006",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")
        request_data = {
            "name": "チーム3",
            "description": "子丑寅卯辰巳",
            "operator_user": "user002",
            "administrators": ["user002", "user003"],
            "members": [
                "user005",
                "user006",
                "user007",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")
        request_data = {
            "name": "チーム4",
            "description": "子寅辰午申戌",
            "operator_user": "user007",
            "administrators": ["user007"],
            "members": [
                "user005",
                "user006",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")
        request_data = {
            "name": "チーム5",
            "description": "申酉戌亥",
            "operator_user": "user007",
            "administrators": ["user007"],
            "members": [
                "user005",
                "user006",
            ],
        }
        url = "/team/"
        response = self.client.post(url, request_data, format="json")

    def test_get_team_list_001(self):
        """
        チーム一覧を取得する
        """
        ans_list = [1]
        _request_data = {
            "operator_user": "user001",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_002(self):
        """
        チーム一覧を取得する
        """
        ans_list = [1, 2, 3]
        _request_data = {
            "operator_user": "user002",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_003(self):
        """
        チーム一覧を取得する
        """
        ans_list = [1, 2, 3]
        _request_data = {
            "operator_user": "user003",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_004(self):
        """
        チーム一覧を取得する
        """
        ans_list = [1, 2]
        _request_data = {
            "operator_user": "user004",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_005(self):
        """
        チーム一覧を取得する
        """
        ans_list = [1, 2, 3, 4, 5]
        _request_data = {
            "operator_user": "user005",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_007(self):
        """
        チーム一覧を取得する
        """
        ans_list = [3, 4, 5]
        _request_data = {
            "operator_user": "user007",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_008(self):
        """
        チーム一覧を取得する
        """
        ans_list = []
        _request_data = {
            "operator_user": "user008",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_sort_changed_at_desc(self):
        """
        チーム一覧を取得する 更新日時でソート
        """
        ans_list = [5, 4, 3, 2, 1]
        _request_data = {
            "operator_user": "user006",
            "order": "DESC",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_name_desc(self):
        """
        チーム一覧を取得する チーム名でソート
        """
        ans_list = [5, 4, 3, 2, 1]
        _request_data = {
            "operator_user": "user006",
            "order": "DESC",
            "sort": "name",
        }
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_search_description_ne(self):
        """
        チーム一覧を取得する チーム説明で検索
        """
        ans_list = [1, 2, 3, 4]
        _request_data = {"operator_user": "user006", "search_keyword": "子"}
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_search_description_ushi(self):
        """
        チーム一覧を取得する チーム説明で検索
        """
        ans_list = [1, 2, 3]
        _request_data = {"operator_user": "user006", "search_keyword": "丑"}
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)

    def test_get_team_list_search_description_i(self):
        """
        チーム一覧を取得する チーム説明で検索
        """
        ans_list = [1, 5]
        _request_data = {"operator_user": "user006", "search_keyword": "亥"}
        url = f"/team/list"
        response = self.client.get(url, _request_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        team_list = [team["id"] for team in response.data]

        self.assertEqual(team_list, ans_list)
