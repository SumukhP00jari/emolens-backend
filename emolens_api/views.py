from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
from rest_framework.parsers import MultiPartParser, FormParser
import re
import json
import whisper
import os

# Connect to OpenRouter using OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY
)

def is_nonsense(text):
    if len(text) < 4:
        return True
    if re.fullmatch(r'[a-zA-Z]{4,}', text):  
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
                data = json.loads(request.body.decode("utf-8"))
        except Exception:
            return Response({
                "error_type": "json_parse_error",
                "message": "Invalid JSON format received from frontend."
            }, status=400)

        input_text = data.get("input_text", "").strip()

        if not input_text:
            return Response({
                "error_type": "empty_input",
                "message": "Please enter a sentence to rephrase."
            }, status=400)

        # First filter: classic gibberish detector
        if is_nonsense(input_text):
            return Response({
                "error_type": "invalid_input",
                "message": "This sentence doesn’t seem meaningful. Please try rephrasing it."
            }, status=400)

        # Second filter: AI checks if it's meaningful
        try:
            check_prompt = f"""
Is the following sentence understandable and not gibberish?

Reply with only "True" or "False".

Sentence: "{input_text}"
"""
            validation_response = client.chat.completions.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": check_prompt}],
                temperature=0,
                max_tokens=5
            )
            ai_check = validation_response.choices[0].message.content.strip().lower()
            if "false" in ai_check:
                return Response({
                    "error_type": "invalid_input",
                    "message": "This sentence doesn’t seem meaningful enough. Please try rephrasing it."
                }, status=400)
        except Exception as e:
            return Response({
                "error_type": "ai_validation_error",
                "message": f"AI validation failed: {str(e)}"
            }, status=500)

        # ✅ Now rephrase the input
        try:
            rephrase_prompt = f"""
You are a kind and supportive parenting assistant.

Please rephrase the following sentence in a way that a 6–8-year-old child can say it to a classmate who may be struggling with emotional regulation or has ADHD.

Make sure the tone is gentle, inclusive, and encourages empathy and friendship.

Avoid sarcasm, judgment, or urgency.

Also keep the response short around 1 or 2 lines and meaningful.

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
        

# Transcribes uploaded audio using Whisper
class TranscribeAudioAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response({"error": "No audio file provided."}, status=400)

        try:
            # Save uploaded audio temporarily
            with open("temp_audio.mp3", "wb") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            model = whisper.load_model("base")  
            result = model.transcribe("temp_audio.mp3")
            transcription = result["text"]

            # Delete temporary file
            os.remove("temp_audio.mp3")

            return Response({
                "transcription": transcription.strip()
            }, status=200)

        except Exception as e:
            return Response({"error": f"Transcription failed: {str(e)}"}, status=500)