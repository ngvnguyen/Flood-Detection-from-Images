"""Dự đoán một ảnh trong thư mục evaluate/."""
import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from config import MODEL_PATH, EVALUATE_DIR, IMAGE_SIZE, CLASSES_PATH

def preprocess_image(file_name):
    image_path = os.path.join(EVALUATE_DIR, file_name)
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Không tìm thấy ảnh tại: {image_path}")
    img = image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array)

def get_class_names():
    if os.path.exists(CLASSES_PATH):
        with open(CLASSES_PATH, "r", encoding="utf-8") as f:
            class_indices = json.load(f)
            return [name for name, _ in sorted(class_indices.items(), key=lambda x: x[1])]
    return ["flooding", "normal"]

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dự đoán ảnh ngập lụt")
    parser.add_argument("image", help="Tên ảnh nằm trong thư mục evaluate/, ví dụ 8.jpg")
    args = parser.parse_args()

    model = tf.keras.models.load_model(MODEL_PATH)
    predictions = model.predict(preprocess_image(args.image), verbose=0)[0]
    class_names = get_class_names()

    result = int(np.argmax(predictions))
    scores_dict = {name: float(score) for name, score in zip(class_names, predictions)}

    print("-" * 40)
    print("Scores:")
    for name, score in scores_dict.items():
        print(f"  {name}: {score:.2%}")
    print("-" * 40)
    print(f"Dự đoán: {class_names[result]} (Độ tin cậy: {predictions[result]:.2%})")
    print("-" * 40)

if __name__ == "__main__":
    main()
