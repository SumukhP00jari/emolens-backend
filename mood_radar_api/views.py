import base64
import io
import numpy as np
import random
from pathlib import Path
from PIL import Image
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from .models import EmotionResponse

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
            top_index = predictions.argmax()
            emotion = EMOTION_LABELS[top_index]
            confidence = float(predictions[top_index])

            try:
                response_obj = EmotionResponse.objects.get(emotion=emotion)
                response = random.choice([response_obj.response1, response_obj.response2])
                response = response if response else response_obj.response1
                meaning = response_obj.meaning
            except EmotionResponse.DoesNotExist:
                response = "No suggested response available."
                meaning = "No meaning found for this emotion."

            result = {
                "predictions": {"emotion": emotion, "confidence": confidence},
                "what_this_might_mean": meaning,
                "how_to_response": response
            }
            return Response(result, status=200)

        except Exception as e:
            return Response({"error": f"Error during prediction: {str(e)}"}, status=500)
