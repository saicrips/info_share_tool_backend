from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound

from ..models import User

from ..serializers import RegisterSerializer


class UserRegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError()

        try:
            with transaction.atomic():
                # 既存ユーザの確認
                username = serializer.validated_data["username"]
                if User.objects.filter(username=username).exists():
                    msg = f"username: {username} was already used"
                    raise ValidationError(msg)

                serializer.save()
        except Exception as e:
            raise e

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class UserDetail(APIView):
    @staticmethod
    def get(request, username):
        if username is None:
            ValidationError()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            msg = f"username: {username} does not found"
            raise NotFound(msg)

        serializer = RegisterSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
