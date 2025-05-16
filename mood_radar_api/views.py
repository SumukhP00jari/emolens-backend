import base64
import io
import numpy as np
from pathlib import Path
from PIL import Image
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

EMOTION_LABELS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
model_path = Path(settings.BASE_DIR) / 'mood_radar_api' / 'emotion_model.h5'

try:
    model = load_model(model_path, compile=False)
    model_loaded = True
except Exception as e:
    print(f"Error loading model: {e}")
    model_loaded = False

class MoodRadarAPIView(APIView):
    def post(self, request):
        if not model_loaded:
            return Response({"error": "Model failed to load. Please try again later."}, status=500)

        base64_str = request.data.get("image_base64")
        if not base64_str:
            return Response({"error": "Missing base64 image string in 'image_base64'"}, status=400)

        try:
            image_data = base64.b64decode(base64_str)
            image = Image.open(io.BytesIO(image_data)).convert("L")
            image = image.resize((48, 48))
            image_array = img_to_array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)

            predictions = model.predict(image_array)[0]
            top3_indices = predictions.argsort()[-3:][::-1]
            results = [
                {"emotion": EMOTION_LABELS[i], "confidence": float(predictions[i])}
                for i in top3_indices
            ]
            return Response({"predictions": results}, status=200)
        except Exception as e:
            return Response({"error": f"Error during prediction: {str(e)}"}, status=500)
