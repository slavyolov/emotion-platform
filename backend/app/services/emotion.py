from typing import Dict

import cv2
import numpy as np
from deepface import DeepFace

MODEL_VERSION = "deepface_emotion_v1"


def predict(image_bytes: bytes) -> Dict:
    """
    Decode image bytes, run DeepFace emotion analysis, and return
    primary_emotion, scores, and model_version.
    """
    # Decode bytes -> OpenCV image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        # Fall back to a neutral prediction if decode fails
        scores = {"neutral": 1.0}
        return {
            "primary_emotion": "neutral",
            "scores": scores,
            "model_version": MODEL_VERSION,
        }

    # DeepFace analyze returns a dict with 'emotion' scores and 'dominant_emotion'[web:80][web:82]
    result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)

    # result can be a list (batch mode) or dict depending on version
    if isinstance(result, list):
        result = result[0]

    emotion_scores = result.get("emotion", {})
    primary_emotion = result.get("dominant_emotion", None)

    if not primary_emotion and emotion_scores:
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
    if not primary_emotion:
        primary_emotion = "neutral"

    # Convert emotion_scores (e.g. numpy types) to plain floats
    scores: Dict[str, float] = {k: float(v) for k, v in emotion_scores.items()}

    return {
        "primary_emotion": primary_emotion,
        "scores": scores,
        "model_version": MODEL_VERSION,
    }