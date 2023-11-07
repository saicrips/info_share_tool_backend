from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from ..models import Team, User, TeamAdministrator, TeamMember


class TeamAdministratorSerializer(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = TeamAdministrator
        fields = ("admin",)


class TeamMemberSerializer(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = TeamMember
        fields = ("member",)


class TeamSerializer(serializers.ModelSerializer):
    administrators = TeamAdministratorSerializer(
        many=True, queryset=User.objects.all(), required=False
    )
    members = TeamMemberSerializer(many=True, queryset=User.objects.all())

    operator_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    def create(self, validated_data):
        admins = validated_data.pop("administrators")
        members = validated_data.pop("members")
        operator_user = validated_data.pop("operator_user")

        team = Team.objects.create(**validated_data)

        # 操作者が管理者に含まれないとき追加する
        if operator_user not in admins:
            admins.append(operator_user)
        admin_objs = []
        admins = list(set(admins))
        for admin in admins:
            admin_objs.append(TeamAdministrator(team=team, admin=admin))
        TeamAdministrator.objects.bulk_create(admin_objs)

        member_objs = []
        members = list(set(members))
        for member in members:
            member_objs.append(TeamMember(team=team, member=member))
        TeamMember.objects.bulk_create(member_objs)
        return team

    def update(self, instance: Team, validated_data: dict):
        operator_user = validated_data.pop("operator_user")
        _operator_user = User.objects.filter(username=operator_user).first()

        admins = [
            admin.admin for admin in TeamAdministrator.objects.filter(team=instance)
        ]
        if _operator_user not in admins:
            msg = f"operator: {operator_user} has no permission"
            raise PermissionDenied(msg)

        admins = validated_data.pop("administrators")
        members = validated_data.pop("members")

        instance.name = validated_data.get("name")
        instance.description = validated_data.get("description")

        if operator_user not in admins:
            admins.append(operator_user)
        admin_objs = []
        TeamAdministrator.objects.filter(team=instance).delete()
        for admin in admins:
            admin_objs.append(TeamAdministrator(team=instance, admin=admin))
        TeamAdministrator.objects.bulk_create(admin_objs)

        member_objs = []
        TeamMember.objects.filter(team=instance).delete()
        for member in members:
            member_objs.append(TeamMember(team=instance, member=member))
        TeamMember.objects.bulk_create(member_objs)

        instance.save()
        return instance

    class Meta:
        model = Team
        fields = "__all__"
