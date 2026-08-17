from django.urls import path
from .views import CourseListView,ScenarioListView,AttemptListView,SubmitScenarioView,AdminScenarioView
urlpatterns=[path('courses/',CourseListView.as_view()),path('scenarios/',ScenarioListView.as_view()),path('scenarios/<int:pk>/submit/',SubmitScenarioView.as_view()),path('attempts/me/',AttemptListView.as_view()),path('admin/scenarios/',AdminScenarioView.as_view())]
