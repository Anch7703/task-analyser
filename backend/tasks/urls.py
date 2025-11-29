from django.urls import path
from .views import TaskAnalyzeView, TaskSuggestView

urlpatterns = [
    path("tasks/analyze/", TaskAnalyzeView.as_view()),
    path("tasks/suggest/", TaskSuggestView.as_view()),
]
