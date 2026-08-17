from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course, Scenario, Attempt
from .serializers import CourseSerializer, ScenarioSerializer, AttemptSerializer
from apps.accounts.permissions import IsAdminUser

class CourseListView(generics.ListAPIView):
    queryset=Course.objects.filter(published=True).order_by("order")
    serializer_class=CourseSerializer
    permission_classes=[permissions.AllowAny]

class ScenarioListView(generics.ListAPIView):
    queryset=Scenario.objects.filter(published=True).order_by("id")
    serializer_class=ScenarioSerializer

class AttemptListView(generics.ListAPIView):
    serializer_class=AttemptSerializer
    def get_queryset(self):
        return Attempt.objects.filter(user=self.request.user).select_related("scenario").order_by("-created_at")

class SubmitScenarioView(APIView):
    def post(self, request, pk):
        try:
            scenario=Scenario.objects.get(pk=pk,published=True)
        except Scenario.DoesNotExist:
            return Response({"detail":"Scenario not found."},status=404)
        try:
            choice=int(request.data.get("choice"))
        except (TypeError,ValueError):
            return Response({"detail":"A valid choice is required."},status=400)
        correct=choice==scenario.correct_choice
        points=scenario.points if correct else 0
        Attempt.objects.create(user=request.user,scenario=scenario,selected_choice=choice,correct=correct,points_awarded=points)
        profile=request.user.profile
        if correct:
            profile.points += points
            profile.level=max(1,profile.points//500+1)
            profile.save()
            from apps.gamification.models import Badge,UserBadge
            for badge in Badge.objects.filter(requirement_points__lte=profile.points):
                UserBadge.objects.get_or_create(user=request.user,badge=badge)
        return Response({"correct":correct,"points_awarded":points,"total_points":profile.points,"level":profile.level,"explanation":scenario.explanation})

class AdminScenarioView(generics.ListCreateAPIView):
    queryset=Scenario.objects.all()
    serializer_class=ScenarioSerializer
    permission_classes=[IsAdminUser]
