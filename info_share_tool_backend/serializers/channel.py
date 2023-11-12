from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from .. import models


class ChannelMemberSerializer(serializers.PrimaryKeyRelatedField):
    class Meta:
        model = models.ChannelMember
        fields = ("members",)


class ChannelSerializer(serializers.ModelSerializer):
    members = ChannelMemberSerializer(
        many=True, queryset=models.User.objects.all(), required=False
    )

    operator_user = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all(), write_only=True
    )

    def create(self, validated_data: dict):
        # チームとチーム管理者・メンバ取得
        team = validated_data.get("team")
        team_admins = [
            team_admin.admin.username
            for team_admin in models.TeamAdministrator.objects.filter(team=team)
        ]
        team_members = [
            team_member.member.username
            for team_member in models.TeamMember.objects.filter(team=team)
        ]

        members = validated_data.get("members")
        if validated_data.get("members_scope") == models.Channel.MembersScope.default:
            # 所属するチームの管理者とメンバをチャネルメンバにする
            members = [
                models.User.objects.filter(username=user).first()
                for user in [*team_admins, *team_members]
            ]
        elif validated_data.get("members_scope") == models.Channel.MembersScope.limited:
            if members is not None:
                validated_data.pop("members")
            else:
                raise ValidationError()

        operator_user = validated_data.pop("operator_user")
        _creator = models.User.objects.filter(username=operator_user).first()

        # 操作者が管理者・メンバに含まれないとき権限エラー
        if _creator.username not in [*team_admins, *team_members]:
            msg = f"operator: {operator_user} has no permission"
            raise PermissionDenied(msg)

        channel = models.Channel.objects.create(**validated_data, creator=_creator)

        member_objs = []
        members = list(set(members))
        for member in members:
            member_objs.append(models.ChannelMember(channel=channel, member=member))
        models.ChannelMember.objects.bulk_create(member_objs)

        return channel

    class Meta:
        model = models.Channel
        fields = "__all__"
