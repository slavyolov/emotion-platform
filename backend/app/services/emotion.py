# backend/app/services/emotion.py

from typing import Dict
from io import BytesIO

import numpy as np
from PIL import Image
from deepface import DeepFace

MODEL_VERSION = "deepface_emotion_pillow_v1"


def predict(image_bytes: bytes) -> Dict:
    """
    Decode image bytes with Pillow, run DeepFace emotion analysis,
    and return primary_emotion, scores, and model_version.
    """
    # Decode bytes -> Pillow image in RGB
    try:
        pil_img = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception:
        # Fallback if decode fails
        scores = {"neutral": 1.0}
        return {
            "primary_emotion": "neutral",
            "scores": scores,
            "model_version": MODEL_VERSION,
        }

    # Convert to NumPy array (H, W, 3), RGB ordering[web:118][web:120]
    img = np.array(pil_img, dtype=np.uint8)

    # DeepFace can work directly with this array; enforce_detection=False
    # avoids errors if the face is not perfectly detected.[web:80][web:82]
    result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)

    # DeepFace may return a list or a dict depending on version
    if isinstance(result, list):
        result = result[0]

    emotion_scores = result.get("emotion", {})
    primary_emotion = result.get("dominant_emotion")

    if not primary_emotion and emotion_scores:
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
    if not primary_emotion:
        primary_emotion = "neutral"

    scores: Dict[str, float] = {k: float(v) for k, v in emotion_scores.items()}

    return {
        "primary_emotion": primary_emotion,
        "scores": scores,
        "model_version": MODEL_VERSION,
    }