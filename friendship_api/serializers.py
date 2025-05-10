from rest_framework import serializers
from .models import KindnessTask

class KindnessTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = KindnessTask
        fields = ['task_title', 'task_description']
