from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SimulatorScenario, SimulatorQuestion, SimulatorAnswer
from .serializers import SimulatorScenarioSerializer, SimulatorQuestionSerializer, SimulatorAnswerSerializer


# Returns all scenarios with ID, title, and background
class ScenarioListAPIView(APIView):
    def get(self, request):
        scenarios = SimulatorScenario.objects.all()
        serializer = SimulatorScenarioSerializer(scenarios, many=True)
        return Response(serializer.data)


# Starts a scenario by returning the first question (round 1) and all answer options
class ScenarioStartAPIView(APIView):
    def get(self, request, scenario_id):
        try:
            # Always start from round_num = 1
            question = SimulatorQuestion.objects.get(scenario_id=scenario_id, round_num=1)
            answers = SimulatorAnswer.objects.filter(question_id=question.question_id)
            question_data = SimulatorQuestionSerializer(question).data
            answer_data = SimulatorAnswerSerializer(answers, many=True).data
            return Response({"question": question_data, "answers": answer_data})
        except SimulatorQuestion.DoesNotExist:
            return Response({"error": "Scenario not found or no round 1 question."}, status=404)


# Given an answer ID, returns the next question and its answer options
class NextRoundAPIView(APIView):
    def post(self, request):
        answer_id = request.data.get("answer_id")
        # next_round_num
        try:
            selected_answer = SimulatorAnswer.objects.get(answer_id=answer_id)
            next_q_id = selected_answer.next_question_id

            if not next_q_id:
                return Response({"message": "Simulation complete."})

            next_question = SimulatorQuestion.objects.get(question_id=next_q_id)
            answers = SimulatorAnswer.objects.filter(question_id=next_q_id)

            question_data = SimulatorQuestionSerializer(next_question).data
            answer_data = SimulatorAnswerSerializer(answers, many=True).data

            return Response({"question": question_data, "answers": answer_data})

        except SimulatorAnswer.DoesNotExist:
            return Response({"error": "Answer not found."}, status=404)
        except SimulatorQuestion.DoesNotExist:
            return Response({"error": "Next question not found."}, status=404)

