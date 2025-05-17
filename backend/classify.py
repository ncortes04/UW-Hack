import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

MODEL_PATH = "skin_disease_classifier.keras"
CLASS_NAMES_FILE = "class_names.txt"
IMG_SIZE = (224, 224)

if not os.path.exists(CLASS_NAMES_FILE):
    raise FileNotFoundError("❌ class_names.txt not found. Please make sure you saved it during training.")

with open(CLASS_NAMES_FILE, "r") as f:
    class_names = [line.strip() for line in f]

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"❌ Model file not found at: {MODEL_PATH}")
    print("🔍 Loading model...")
    return tf.keras.models.load_model(MODEL_PATH)

def classify_skin_image(model, img_path):
    if not os.path.exists(img_path):
        print(f"❌ Image not found at: {img_path}")
        return None, None

    print(f"📷 Classifying image: {img_path}")
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)[0] 
    print(f"🔍 Model prediction: {predictions}")
    print("\n📊 All class confidences:")
    for i, prob in enumerate(predictions):
        print(f"{class_names[i]:<30}: {prob * 100:.2f}%")

    predicted_index = np.argmax(predictions)
    predicted_class = class_names[predicted_index]
    confidence = predictions[predicted_index]

    return predicted_class, confidence
