from rest_framework import serializers
from .models import (
    ADHD, Neurodivergent, LearningHub, AdhdTreatment, AdhdPrevalenceYear, AdhdPrevalenceAge,
    AdhdPrescription, AdhdDisorder, AdhdCondition, AdhdDayoff
)
# Serializers convert model instances into JSON and vice versa
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

class AdhdTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdTreatment
        fields = '__all__'

class AdhdPrevalenceYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdPrevalenceYear
        fields = '__all__'

class AdhdPrevalenceAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdPrevalenceAge
        fields = '__all__'

class AdhdPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdPrescription
        fields = '__all__'

class AdhdDisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdDisorder
        fields = '__all__'

class AdhdConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdCondition
        fields = '__all__'

class AdhdDayoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdhdDayoff
        fields = '__all__'