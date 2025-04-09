from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
import re
import json

# Connect to OpenRouter using OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY
)

class RephraseTextAPIView(APIView):
    def post(self, request):
        try:
            # Handle malformed JSON edge cases
            data = request.data
            if not isinstance(data, dict):
                data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return Response({
                "error_type": "json_parse_error",
                "message": "Invalid JSON format received from frontend."
            }, status=400)

        input_text = data.get("input_text", "").strip()

        if not input_text or len(input_text) < 4:
            return Response({
                "error_type": "empty_input",
                "message": "Please enter a longer, more meaningful sentence."
            }, status=400)

        try:
            # ✅ STEP 1: Validate using AI
            validation_prompt = f"""
You're a friendly parenting assistant.

Check if the following sentence is understandable and simple enough for a 6–8-year-old child to say to a classmate.

Be forgiving. If it's a basic sentence with some meaning, say "Yes".

Reply only with "Yes" or "No".

Sentence: "{input_text}"
"""
            validation_response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": validation_prompt}],
                temperature=0,
                max_tokens=5
            )

            ai_validation = validation_response.choices[0].message.content.strip().lower()

            if "no" in ai_validation:
                return Response({
                    "error_type": "invalid_input",
                    "message": "This sentence doesn’t seem meaningful enough. Please try rephrasing it."
                }, status=400)

            # ✅ STEP 2: Rephrase if valid
            rephrase_prompt = f"""
You are a kind and supportive parenting assistant.

Please rephrase the following sentence in a way that a 6–8-year-old child can say it to a classmate who may be struggling with emotional regulation or has ADHD.

Make sure the tone is gentle, inclusive, and encourages empathy and friendship.

Avoid sarcasm, judgment, or urgency.

Original: "{input_text}"
Rephrased:
"""
            rephrase_response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": rephrase_prompt}],
                temperature=0.7,
                max_tokens=150
            )

            output = rephrase_response.choices[0].message.content.strip()

            return Response({
                "original": input_text,
                "rephrased": output
            }, status=200)

        except Exception as e:
            return Response({
                "error_type": "server_error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=500)