from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied

from ..models import Channel, User, ChannelMember, TeamAdministrator

from ..serializers import ChannelSerializer


class ChannelCreateView(APIView):
    @staticmethod
    def post(request):
        serializer = ChannelSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class ChannelDetailView(APIView):
    @staticmethod
    def get(request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            msg = f"channel: id {channel_id} does not found"
            raise NotFound(msg)

        operator_user = request.GET.get("operator_user")
        _operator_user = User.objects.filter(username=operator_user).first()

        members = [member.member for member in ChannelMember.objects.filter(channel=channel)]
        refferer_users = members
        if _operator_user not in refferer_users:
            msg = f"operator user: {operator_user} has no permision for channel: {channel_id}"
            raise PermissionDenied(msg)

        serializer = ChannelSerializer(channel)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def put(request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            msg = f"channel: id {channel_id} does not found"
            raise NotFound(msg)

        serializer = ChannelSerializer(channel, data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def delete(request, channel_id):
        try:
            channel = Channel.objects.get(id=channel_id)
        except Channel.DoesNotExist:
            msg = f"channel: id {channel_id} does not found"
            raise NotFound(msg)

        operator_user = request.data.get("operator_user")
        _operator_user = User.objects.filter(username=operator_user).first()

        admins = [admin.admin for admin in TeamAdministrator.objects.filter(team=channel.team)]
        if _operator_user not in admins:
            msg = f"operator: {operator_user} has no permission"
            raise PermissionDenied(msg)

        channel.delete()

        return Response(
            {},
            status=status.HTTP_200_OK,
        )
