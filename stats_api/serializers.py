from rest_framework import serializers
from .models import (
    ADHD, Neurodivergent, LearningHub, ADHDTreatment,
    ADHDPrevalenceYear, ADHDPrevalenceAge,
    ADHDPrescription, ADHDDisorder, ADHDCondition, ADHDDayoff
)
class ADHDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHD
        fields = '__all__'

class NeurodivergentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neurodivergent
        fields = '__all__'

class LearningHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningHub
        fields = '__all__'

class ADHDTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDTreatment
        fields = '__all__'

class ADHDPrevalenceYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDPrevalenceYear
        fields = '__all__'

class ADHDPrevalenceAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDPrevalenceAge
        fields = '__all__'

class ADHDPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDPrescription
        fields = '__all__'

class ADHDDisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDDisorder
        fields = '__all__'

class ADHDConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDCondition
        fields = '__all__'

class ADHDDayoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDDayoff
        fields = '__all__'
