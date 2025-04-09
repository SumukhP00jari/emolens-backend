from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
import re

# Connect to OpenRouter using OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY
)

class RephraseTextAPIView(APIView):
    def post(self, request):
        input_text = request.data.get("input_text", "").strip()

        if not input_text or len(input_text) < 4:
            return Response({
                "error_type": "empty_or_short",
                "message": "Please enter a longer, more meaningful sentence."
            }, status=400)

        try:
            # Step 1: Ask AI if the sentence is meaningful
            validation_prompt = f"""
Is the following sentence meaningful and appropriate to be spoken by a child aged 6 to 8 to a classmate?

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
                    "error_type": "nonsensical_input",
                    "message": "The sentence does not seem meaningful or appropriate."
                }, status=400)

            # Step 2: If valid, rephrase it nicely
            rephrase_prompt = f"""
You are a kind and supportive parenting assistant.

Please rephrase the following sentence in a way that a 6–8-year-old child can say it to a classmate who may be struggling with emotional regulation or has ADHD.

Make sure the tone is gentle, inclusive, and encourages empathy and friendship.

Avoid sarcasm, judgment, or urgency.

Original: "{input_text}"
Rephrased:
"""
            completion = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": rephrase_prompt}],
                temperature=0.7,
                max_tokens=150
            )

            output = completion.choices[0].message.content.strip()

            return Response({
                "original": input_text,
                "rephrased": output
            }, status=200)

        except Exception as e:
            return Response({
                "error_type": "server_error",
                "message": f"An unexpected error occurred: {str(e)}"
            }, status=500)
