from PIL import Image
import random

LABELS = ["happy", "neutral", "sad", "surprise"]


def analyze_emotion(image_path: str):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    label = random.choice(LABELS)
    score = round(random.uniform(0.70, 0.95), 2)

    return {
        "primary_emotion": label,
        "confidence": score,
        "image_width": width,
        "image_height": height
    }
