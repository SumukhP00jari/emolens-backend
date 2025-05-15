from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EmotionGuessing
from .serializers import EmotionGuessingSerializer

class EmotionGuessingAPIView(APIView):
    def get(self, request):
        question_ids = EmotionGuessing.objects.values_list('question_id', flat=True).distinct()
        response_data = []

        for qid in question_ids:
            question_entries = EmotionGuessing.objects.filter(question_id=qid)
            if not question_entries.exists():
                continue

            options = [
                {
                    "answer_id": entry.answer_id,
                    "answer_desc": entry.answer_desc
                }
                for entry in question_entries
            ]

            image_url = question_entries.first().image_url
            correct_answer_id = question_entries.first().correct_answer_id

            response_data.append({
                "question_id": qid,
                "image_url": image_url,
                "options": options,
                "correct_answer_id": correct_answer_id
            })

        return Response(response_data)