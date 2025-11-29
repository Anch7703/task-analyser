from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    title = serializers.CharField()
    due_date = serializers.DateField(required=False, allow_null=True)
    estimated_hours = serializers.FloatField(required=False, allow_null=True)
    importance = serializers.IntegerField(required=False, allow_null=True, min_value=1, max_value=10)
    dependencies = serializers.ListField(child=serializers.CharField(), required=False)

class TaskAnalyzeRequestSerializer(serializers.Serializer):
    strategy = serializers.ChoiceField(
        choices=["fastest_wins", "high_impact", "deadline_driven", "smart_balance"],
        default="smart_balance",
    )
    tasks = TaskInputSerializer(many=True)

class ScoredTaskSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    due_date = serializers.DateField(allow_null=True)
    estimated_hours = serializers.FloatField(allow_null=True)
    importance = serializers.IntegerField(allow_null=True)
    dependencies = serializers.ListField(child=serializers.CharField())
    score = serializers.FloatField()
    explanation = serializers.CharField()
    has_circular_dependency = serializers.BooleanField()
