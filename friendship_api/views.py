from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import KindnessTask
from .serializers import KindnessTaskSerializer

# API endpoint to fetch all kindness tasks
class KindnessTaskAPIView(APIView):
    def get(self, request):
        tasks = KindnessTask.objects.all()
        serializer = KindnessTaskSerializer(tasks, many=True)
        return Response(serializer.data)
