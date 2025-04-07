from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI

# Connect to OpenRouter using OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY
)

class RephraseTextAPIView(APIView):
    def post(self, request):
        input_text = request.data.get("input_text")
        if not input_text:
            return Response({"error": "Input text is required."}, status=400)

        try:
            # Chat-style prompt for better context understanding
            prompt = f"""
You are a kind and supportive parenting assistant.
Rephrase the following sentence to sound gentle, emotionally safe, and suitable for a 6–8-year-old child.

Avoid judgment, sarcasm, or urgency.

Original: "{input_text}"
Rephrased:
"""

            # Use a model that works well with messages (ChatML)
            completion = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",  # Updated model name
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )

            output = completion.choices[0].message.content.strip()

            return Response({
                "original": input_text,
                "rephrased": output
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
