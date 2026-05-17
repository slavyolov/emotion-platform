from typing import Dict

MODEL_VERSION = "stub_fer_v1"


def predict(image_bytes: bytes) -> Dict:
    # Stub implementation returning a constant emotion distribution.
    scores = {"happy": 0.9, "sad": 0.05, "neutral": 0.05}
    primary = max(scores, key=scores.get)
    return {
        "primary_emotion": primary,
        "scores": scores,
        "model_version": MODEL_VERSION,
    }
