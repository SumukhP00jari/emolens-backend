from django.shortcuts import render

import os
import numpy as np
import cv2
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from tensorflow.keras.models import load_model

# Load the model only once when the server starts
model_path = os.path.join(settings.BASE_DIR, "mood_radar_api", "emotion_model.h5")
model = load_model(model_path, compile=False)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class MoodRadarAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image file provided."}, status=400)

        try:
            # Read image file as byte array
            file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img is None:
                return Response({"error": "Invalid image format."}, status=400)

            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Detect faces
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) == 0:
                return Response({"error": "No face detected."}, status=400)
            if len(faces) > 1:
                return Response({"error": "Please upload a photo with only ONE person."}, status=400)

            # Process the first face found
            x, y, w, h = faces[0]
            face_img = gray[y:y + h, x:x + w]
            face_img = cv2.resize(face_img, (48, 48))
            face_array = face_img.astype("float32") / 255.0
            face_array = np.expand_dims(face_array, axis=-1)
            face_array = np.expand_dims(face_array, axis=0)

            # Predict emotion
            prediction = model.predict(face_array)
            predicted_index = int(np.argmax(prediction))
            emotion = emotion_labels[predicted_index]
            confidence = float(np.max(prediction)) * 100

            return Response({
                "emotion": emotion,
                "confidence_percent": round(confidence, 2)
            }, status=200)

        except Exception as e:
            return Response({"error": f"Emotion detection failed: {str(e)}"}, status=500)
