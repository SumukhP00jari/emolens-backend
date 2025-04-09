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
    if len(text) < 4:
        return True
    if re.fullmatch(r'[a-zA-Z]{4,}', text):  # single clean word is okay
        return False
    if re.fullmatch(r'[^a-zA-Z0-9 ]+', text):  # just symbols
        return True
    if not re.search(r'[aeiouAEIOU]', text):  # no vowels = gibberish
        return True
    if len(re.findall(r'[a-zA-Z]', text)) / len(text) < 0.5:
        return True
    return False


class RephraseTextAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            if not isinstance(data, dict):
                data = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            return Response({
                "error_type": "json_parse_error",
                "message": "Invalid JSON format received from frontend."
            }, status=400)
        input_text = request.data.get("input_text", "").strip()

        # Quick check: empty or obviously nonsensical
        if not input_text:
            return Response({
                "error_type": "empty_input",
                "message": "Please enter a sentence to rephrase."
            }, status=400)

        if is_nonsense(input_text):
            return Response({
                "error_type": "nonsense_check",
                "message": "The text seems nonsensical. Please enter a meaningful sentence."
            }, status=400)

        try:
            # Step 1: Validate with AI — is it a meaningful and age-appropriate sentence?
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
                    "error_type": "not_meaningful",
                    "message": "The sentence does not seem meaningful or appropriate for a child to say."
                }, status=400)

            # Step 2: Generate rephrased child-friendly sentence
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