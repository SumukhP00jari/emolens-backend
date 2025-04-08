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

def is_nonsense(text):
    if len(text.strip()) < 4:
        return True
    if re.fullmatch(r'[a-zA-Z]{4,}', text):  # a valid single word like "Hello"
        return False
    if re.fullmatch(r'[^a-zA-Z0-9 ]+', text):  # only symbols
        return True
    if not re.search(r'[aeiouAEIOU]', text):  # no vowels
        return True
    if len(re.findall(r'[a-zA-Z]', text)) / max(1, len(text)) < 0.5:  # mostly non-letters
        return True
    return False

class RephraseTextAPIView(APIView):
    def post(self, request):
        input_text = request.data.get("input_text")

        # Input validation
        if not input_text or is_nonsense(input_text):
            return Response({
                "error": "The text seems nonsensical. Please enter a meaningful sentence."
            }, status=400)

        # Updated empathetic rephrasing prompt
        prompt = f"""
        You are a kind and supportive parenting assistant.

        Please rephrase the following sentence in a way that a 6–8-year-old child can say it to a classmate who may be struggling with emotional regulation or has ADHD.

        Make sure the tone is gentle, inclusive, and encourages empathy and friendship.

        Avoid sarcasm, judgment, or urgency.

        Original: "{input_text}"
        Rephrased:
        """

        try:
            completion = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
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
