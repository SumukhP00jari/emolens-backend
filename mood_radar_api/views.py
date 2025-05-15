import os
import cv2
import h5py
import json
import numpy as np
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from keras.models import model_from_json

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

model_path = os.path.join(os.path.dirname(__file__), "emotion_model.h5")

def clean_layer_config(config):
    if isinstance(config, dict):
        config.pop("batch_shape", None)
        config.pop("dtype_policy", None)
        config.pop("synchronized", None)
        for value in config.values():
            clean_layer_config(value)
    elif isinstance(config, list):
        for item in config:
            clean_layer_config(item)

def load_emotion_model(h5_path):
    try:
        with h5py.File(h5_path, "r") as f:
            model_config = f.attrs.get("model_config")
            if isinstance(model_config, bytes):
                model_config = model_config.decode("utf-8")

            config_dict = json.loads(model_config)
            clean_layer_config(config_dict)
            clean_json = json.dumps(config_dict)

            model = model_from_json(clean_json)
            model.load_weights(h5_path)
            print("✅ Emotion model loaded successfully.")
            return model
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return None

model = load_emotion_model(model_path)

class MoodRadarAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        if model is None:
            return Response({"error": "Model failed to load. Please try again later."}, status=500)

        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"error": "No image uploaded"}, status=400)

        try:
            img_array = np.frombuffer(image_file.read(), np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            if img is None:
                return Response({"error": "Invalid image format"}, status=400)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(faces) == 0:
                return Response({"error": "No face detected"}, status=400)
            if len(faces) > 1:
                return Response({"error": "Multiple faces detected. Upload one face at a time."}, status=400)

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
            return Response({"error": f"Internal error during emotion detection: {str(e)}"}, status=500)
