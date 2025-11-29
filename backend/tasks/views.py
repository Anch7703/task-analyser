from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import TaskAnalyzeRequestSerializer, ScoredTaskSerializer
from .scoring import analyze_tasks
from .models import Task


class TaskAnalyzeView(APIView):
    def post(self, request):
        serializer = TaskAnalyzeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        strategy = serializer.validated_data["strategy"]
        tasks_data = serializer.validated_data["tasks"]

        scored = analyze_tasks(tasks_data, strategy=strategy)

        Task.objects.all().delete()
        for s in scored:
            t = s.task
            Task.objects.create(
                title=t.title,
                due_date=t.due_date,
                estimated_hours=t.estimated_hours,
                importance=t.importance,
                dependencies=t.dependencies,
                last_score=s.score,
                last_strategy=strategy,
            )

        output = [
            {
                "id": s.task.id,
                "title": s.task.title,
                "due_date": s.task.due_date,
                "estimated_hours": s.task.estimated_hours,
                "importance": s.task.importance,
                "dependencies": s.task.dependencies,
                "score": s.score,
                "explanation": s.explanation,
                "has_circular_dependency": s.has_circular_dependency,
            }
            for s in scored
        ]
        return Response(output, status=status.HTTP_200_OK)


class TaskSuggestView(APIView):
    def get(self, request):
        strategy = request.query_params.get("strategy", "smart_balance")
        limit = int(request.query_params.get("limit", 3))

        raw = []
        for i, t in enumerate(Task.objects.all()):
            raw.append(
                {
                    "id": str(i),
                    "title": t.title,
                    "due_date": t.due_date,
                    "estimated_hours": t.estimated_hours,
                    "importance": t.importance,
                    "dependencies": t.dependencies,
                }
            )

        scored = analyze_tasks(raw, strategy=strategy)
        top = scored[:limit]

        output = [
            {
                "id": s.task.id,
                "title": s.task.title,
                "due_date": s.task.due_date,
                "estimated_hours": s.task.estimated_hours,
                "importance": s.task.importance,
                "dependencies": s.task.dependencies,
                "score": s.score,
                "explanation": s.explanation,
                "has_circular_dependency": s.has_circular_dependency,
            }
            for s in top
        ]

        return Response(output, status=status.HTTP_200_OK)
