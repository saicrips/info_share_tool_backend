from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from ..models import Team, TeamAdministrator, TeamMember, User

from ..serializers import TeamSerializer


class TeamCreateView(APIView):
    @staticmethod
    def post(request):
        serializer = TeamSerializer(data=request.data)

        if not serializer.is_valid():
            print(serializer.errors)
            raise ValidationError(serializer.errors)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class TeamDetailView(APIView):
    @staticmethod
    def get(request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            msg = f"team: id {team_id} does not found"
            raise NotFound(msg)

        operator_user = request.GET.get("operator_user")
        _operator_user = User.objects.filter(username=operator_user).first()

        admins = [admin.admin for admin in TeamAdministrator.objects.filter(team=team)]
        members = [member.member for member in TeamMember.objects.filter(team=team)]
        refferer_users = [*admins, *members]
        if _operator_user not in refferer_users:
            msg = f"operator user: {operator_user} has no permision for team: {team_id}"
            raise PermissionDenied(msg)

        serializer = TeamSerializer(team)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def put(request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            msg = f"team: id {team_id} does not found"
            raise NotFound(msg)

        serializer = TeamSerializer(team, data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        try:
            serializer.save()
        except Exception as e:
            raise e

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def delete(request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            msg = f"team: id {team_id} does not found"
            raise NotFound(msg)

        operator_user = request.data.get("operator_user")
        _operator_user = User.objects.filter(username=operator_user).first()

        admins = [admin.admin for admin in TeamAdministrator.objects.filter(team=team)]
        if _operator_user not in admins:
            msg = f"operator: {operator_user} has no permission"
            raise PermissionDenied(msg)

        team.delete()

        return Response(
            {},
            status=status.HTTP_200_OK,
        )


class TeamListView(APIView):
    @staticmethod
    def get(request):
        operator_user = request.GET.get("operator_user")
        _operator_user = User.objects.filter(username=operator_user).first()

        sort = request.GET.get("sort")
        if sort is None:
            sort = "changed_at"
        order = request.GET.get("order")
        if order == "ASC":
            _order = ""
        elif order == "DESC":
            _order = "-"
        else:
            _order = ""

        search_keyword = request.GET.get("search_keyword")

        conditions = []
        admins_condition = Q(administrators=_operator_user)
        members_condition = Q(members=_operator_user)
        conditions.append(admins_condition | members_condition)

        if search_keyword is not None:
            name_search_condition = Q(name__icontains=search_keyword)
            description_search_condition = Q(description__icontains=search_keyword)
            conditions.append(name_search_condition | description_search_condition)

        queryset = Team.objects.filter(*conditions)
        orders = ["changed_at"]
        if order is not None:
            orders.insert(0, _order + sort)
        queryset = queryset.order_by(*orders)

        serializer = TeamSerializer(queryset.distinct(), many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
