from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

from ..models import Channel

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
