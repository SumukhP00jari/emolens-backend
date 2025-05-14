from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

import numpy as np
import cv2
from tensorflow.keras.models import load_model
import os
import tempfile

# Load model and labels
model_path = os.path.join(os.path.dirname(__file__), "emotion_model.h5")
model = load_model(model_path)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class MoodRadarAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'No image uploaded.'}, status=400)

        try:
            # Save the image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                for chunk in image_file.chunks():
                    tmp.write(chunk)
                img_path = tmp.name

            # Load and process image
            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            os.remove(img_path)  # Clean up

            if len(faces) == 0:
                return Response({'error': 'No face detected.'}, status=200)

            for (x, y, w, h) in faces[:1]:  # First face only
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (48, 48))
                face_array = face_img.astype("float32") / 255.0
                face_array = np.expand_dims(face_array, axis=-1)
                face_array = np.expand_dims(face_array, axis=0)

                prediction = model.predict(face_array)
                predicted_class = np.argmax(prediction)
                emotion = emotion_labels[predicted_class]

                return Response({'emotion': emotion}, status=200)

        except Exception as e:
            return Response({'error': f'Processing failed: {str(e)}'}, status=500)