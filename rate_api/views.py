from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
import json

# Connect to OpenRouter using OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY
)

# View to evaluate parent-child conversations using an AI model
class ConversationReviewAPIView(APIView):
    def post(self, request):
        # Step 1: Validate and parse JSON input
        try:
            data = request.data
            if not isinstance(data, dict):
                data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return Response({
                "error_type": "json_parse_error",
                "message": "Invalid JSON format received from frontend."
            }, status=400)

        # Step 2: Check if 'conversation' field is provided
        conversation = data.get("conversation", "").strip()
        if not conversation:
            return Response({
                "error_type": "empty_input",
                "message": "No conversation provided. Please include a conversation string."
            }, status=400)

        try:
            # Step 3: Build prompt for AI evaluation
            prompt = f"""
You are a child-parent communication coach.

Evaluate the following conversation in two parts:

1. Rate it from 1 to 5 based on empathy, clarity, and positive reinforcement.
2. Provide a 2 to 3 line constructive feedback explaining the score.

Conversation:
\"\"\"{conversation}\"\"\"

Please respond using this format:
Rating: X
Feedback: <your feedback>
"""

            # Step 4: Send the prompt to the AI model (Mistral)
            response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=200
            )

            # Step 5: Extract rating and feedback from AI response
            content = response.choices[0].message.content.strip()
            lines = content.splitlines()
            rating_line = next((line for line in lines if "Rating:" in line), "Rating: 3")
            feedback_lines = [line.replace("Feedback:", "").strip() for line in lines if "Feedback:" in line or "Rating:" not in line]

            rating = rating_line.split(":")[1].strip()
            feedback = " ".join(feedback_lines)

            # Step 6: Return the result to frontend
            return Response({
                "rating": rating,
                "feedback": feedback
            }, status=200)

        # Step 7: Catch any unexpected server/AI errors
        except Exception as e:
            return Response({
                "error_type": "ai_response_error",
                "message": f"AI processing failed: {str(e)}"
            }, status=500)