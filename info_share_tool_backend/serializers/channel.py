from rest_framework import fields, serializers
from ..models import (
    Team,
    User,
    TeamAdministrator,
    TeamMember,
    Channel,
    ChannelShareUser,
)


class ChannelShareUserSerializer(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = ChannelShareUser
        fields = ("share_user",)


class ChannelSerializer(serializers.ModelSerializer):
    share_users = ChannelShareUserSerializer(
        many=True, queryset=User.objects.all(), required=False
    )

    creator = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    def create(self, validated_data):
        share_users = validated_data.pop("share_users")
        creator = validated_data.get("creator")

        team = Channel.objects.create(**validated_data)

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
