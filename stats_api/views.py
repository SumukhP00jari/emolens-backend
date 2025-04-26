from django.shortcuts import render

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    ADHD, Neurodivergent, LearningHub, ADHDTreatment, ADHDDisorder,
    ADHDPrevalenceYear, ADHDPrevalenceAge, ADHDPrescription, ADHDCondition, ADHDDayOff
)
from .serializers import (
    ADHDSerializer, NeurodivergentSerializer, LearningHubSerializer, ADHDTreatmentSerializer,
    ADHDDisorderSerializer, ADHDPrevalenceYearSerializer, ADHDPrevalenceAgeSerializer,
    ADHDPrescriptionSerializer, ADHDConditionSerializer, ADHDDayOffSerializer
)

class ADHDStatsAPIView(APIView):
    def get(self, request):
        data = ADHD.objects.all()
        serializer = ADHDSerializer(data, many=True)
        return Response(serializer.data)

class NeurodivergentStatsAPIView(APIView):
    def get(self, request):
        data = Neurodivergent.objects.all()
        serializer = NeurodivergentSerializer(data, many=True)
        return Response(serializer.data)
    
class LearningHubAPIView(APIView):
    def get(self, request):
        data = LearningHub.objects.all()
        serializer = LearningHubSerializer(data, many=True)
        return Response(serializer.data)


class ADHDTreatmentAPIView(APIView):
    def get(self, request):
        data = ADHDTreatment.objects.all()
        serializer = ADHDTreatmentSerializer(data, many=True)
        return Response(serializer.data)


class ADHDPrevalenceYearAPIView(APIView):
    def get(self, request):
        data = ADHDPrevalenceYear.objects.all()
        serializer = ADHDPrevalenceYearSerializer(data, many=True)
        return Response(serializer.data)


class ADHDPrevalenceAgeAPIView(APIView):
    def get(self, request):
        data = ADHDPrevalenceAge.objects.all()
        serializer = ADHDPrevalenceAgeSerializer(data, many=True)
        return Response(serializer.data)


class ADHDDisorderAPIView(APIView):
    def get(self, request):
        data = ADHDDisorder.objects.all()
        serializer = ADHDDisorderSerializer(data, many=True)
        return Response(serializer.data)


class ADHDConditionAPIView(APIView):
    def get(self, request):
        data = ADHDCondition.objects.all()
        serializer = ADHDConditionSerializer(data, many=True)
        return Response(serializer.data)


class ADHDDayOffAPIView(APIView):
    def get(self, request):
        data = ADHDDayOff.objects.all()
        serializer = ADHDDayOffSerializer(data, many=True)
        return Response(serializer.data)


class ADHDPrescriptionAPIView(APIView):
    def get(self, request):
        data = ADHDPrescription.objects.all()
        serializer = ADHDPrescriptionSerializer(data, many=True)
        return Response(serializer.data)

class DBConnectionCheck(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                tables = cursor.fetchall()
            return Response({"status": "connected", "tables": tables})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)