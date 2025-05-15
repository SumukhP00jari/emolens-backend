import os
import cv2
import numpy as np
import json
import h5py
from tensorflow.keras.models import model_from_json
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def load_emotion_model(h5_path):
    with h5py.File(h5_path, "r") as f:
        model_config = f.attrs["model_config"]
        if isinstance(model_config, bytes):
            model_config = model_config.decode("utf-8")

        model_dict = json.loads(model_config)
        for layer in model_dict.get("config", {}).get("layers", []):
            if "config" in layer and "batch_shape" in layer["config"]:
                del layer["config"]["batch_shape"]

        cleaned_json = json.dumps(model_dict)
        model = model_from_json(cleaned_json)
        model.load_weights(h5_path)
    return model

model_path = os.path.join(os.path.dirname(__file__), "emotion_model.h5")
model = load_emotion_model(model_path)

class MoodRadarAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image uploaded"}, status=400)

        try:
            img_array = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) == 0:
                return Response({"error": "No face detected"}, status=400)
            elif len(faces) > 1:
                return Response({"error": "Please upload an image with only one face"}, status=400)

            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (48, 48))

            face_array = face_img.astype("float32") / 255.0
            face_array = np.expand_dims(face_array, axis=-1)
            face_array = np.expand_dims(face_array, axis=0)

            prediction = model.predict(face_array)
            emotion = emotion_labels[np.argmax(prediction)]

            return Response({"emotion": emotion}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
