from rest_framework import serializers
from .models import ADHD, Neurodivergent

class ADHDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHD
        fields = '__all__'

class NeurodivergentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neurodivergent
        fields = '__all__'