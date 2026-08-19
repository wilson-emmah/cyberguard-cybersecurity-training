from django.contrib.auth.models import User

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsAdminUser
from .serializers import RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            UserSerializer(request.user).data,
            status=status.HTTP_200_OK
        )


class AdminUsersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.all().order_by("-date_joined")

        return Response(
            UserSerializer(users, many=True).data,
            status=status.HTTP_200_OK
        )


class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        from apps.training.models import Scenario, Attempt

        return Response({
            "users": User.objects.count(),
            "scenarios": Scenario.objects.count(),
            "attempts": Attempt.objects.count(),
        })
