from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import LoginSerializer, UserSerializer


class UserLoginAPI(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            serializer = UserSerializer(instance=self.request.user)
            return Response(serializer.data)
        else:
            return Response({}, status=status.HTTP_403_FORBIDDEN)

    def post(self, *args, **kwargs):
        serializer = LoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if user:
            login(self.request, user)
            return Response({"msg": "logined"})

        return Response(
            {"msg": "아이디나 비밀번호가 올바르지 않습니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def delete(self, *args, **kwargs):
        logout(self.request)
        return Response({"msg": "logout"})
