import io
import numpy as np
import random
import cv2
from pathlib import Path
from PIL import Image
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from deepface import DeepFace
from .models import EmotionResponse

cascade_path = Path(settings.BASE_DIR) / 'mood_radar_api' / 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(str(cascade_path))

def formatted_error(error_type, message, status_code=400):
    return Response({
        "error_type": error_type,
        "message": message
    }, status=status_code)

class MoodRadarAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return formatted_error("missing_input", "Missing image file in 'image' field.")

        try:
            image = Image.open(image_file).convert("L")
            image_cv = np.array(image)

            faces = face_cascade.detectMultiScale(image_cv, scaleFactor=1.1, minNeighbors=5)
            if len(faces) == 0:
                return formatted_error("face_not_detected", "No human face detected in the image.")
            elif len(faces) > 1:
                return formatted_error("multiple_faces_detected", "Please upload a photo with only one human face.")

            image_rgb = Image.open(image_file).convert("RGB")
            img_array = np.array(image_rgb)

            analysis = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=False)[0]
            emotion = analysis['dominant_emotion'].capitalize()
            confidence = analysis['emotion'][emotion.lower()] / 100.0  

            try:
                response_obj = EmotionResponse.objects.get(emotion__iexact=emotion)
                response = random.choice([response_obj.response1, response_obj.response2])
                response = response if response else response_obj.response1
                meaning = response_obj.meaning
            except EmotionResponse.DoesNotExist:
                response = "No suggested response available."
                meaning = "No meaning found for this emotion."

            return Response({
                "success": True,
                "predictions": {"emotion": emotion, "confidence": round(confidence, 4)},
                "what_this_might_mean": meaning,
                "how_to_response": response
            }, status=200)

        except Exception as e:
            return formatted_error("server_error", f"An unexpected error occurred: {str(e)}", 500)
