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
    
    def update(self, instance: models.Channel, validated_data: dict):
        operator_user = validated_data.pop("operator_user")
        _operator_user = models.User.objects.filter(username=operator_user).first()

        admins = [
            admin.admin for admin in models.TeamAdministrator.objects.filter(team=instance.team)
        ]
        if _operator_user not in admins:
            msg = f"operator: {operator_user} has no permission"
            raise PermissionDenied(msg)

        instance.name = validated_data.get("name")
        instance.description = validated_data.get("description")
        
        members = validated_data.pop("members")
        models.ChannelMember.objects.filter(channel=instance).delete()
        user_objs = models.User.objects.filter(username__in=members)
        member_objs = [
            models.ChannelMember(channel=instance, member=user_obj) 
            for user_obj in user_objs
        ]

        models.ChannelMember.objects.bulk_create(member_objs)

        instance.save()
        return instance

    class Meta:
        model = models.Channel
        fields = "__all__"
