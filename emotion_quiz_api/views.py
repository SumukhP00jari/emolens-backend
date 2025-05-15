from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response

class EmotionGuessingAPIView(APIView):
    def get(self, request):
        print(" EmotionGuessing API using correct column names")

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT question_id, image_url, answer_id, answer_desc, correct_answer
                    FROM emotion_guessing
                """)
                rows = cursor.fetchall()

            grouped = {}
            for question_id, image_url, answer_id, answer_desc, correct_answer in rows:
                if question_id not in grouped:
                    grouped[question_id] = {
                        "question_id": question_id,
                        "image_url": image_url,
                        "options": [],
                        "correct_answer_id": correct_answer  
                    }

                grouped[question_id]["options"].append({
                    "id": answer_id,
                    "desc": answer_desc
                })

            return Response(list(grouped.values()))

        except Exception as e:
            return Response({"error": str(e)}, status=500)
