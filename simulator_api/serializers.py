from rest_framework import serializers
from .models import SimulatorScenario, SimulatorQuestion, SimulatorAnswer

class SimulatorScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorScenario
        fields = ['scenario_id', 'scenario_title', 'background']

class SimulatorAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimulatorAnswer
        fields = ['answer_id', 'answer_text', 'emotion_indicate', 'next_question_id']

class SimulatorQuestionSerializer(serializers.ModelSerializer):
    answers = SimulatorAnswerSerializer(many=True, source='simulatoranswer_set')

    class Meta:
        model = SimulatorQuestion
        fields = ['question_id', 'round_num', 'question_text', 'answers']
