"""Dự đoán một ảnh trong thư mục evaluate/."""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from config import MODEL_PATH, EVALUATE_DIR, IMAGE_SIZE

def preprocess_image(file_name):
    image_path = os.path.join(EVALUATE_DIR, file_name)
    img = image.load_img(image_path, target_size=IMAGE_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Dự đoán ảnh ngập lụt")
    parser.add_argument("image", help="Tên ảnh nằm trong thư mục evaluate/, ví dụ 8.jpg")
    args = parser.parse_args()

    model = tf.keras.models.load_model(MODEL_PATH)
    predictions = model.predict(preprocess_image(args.image), verbose=0)[0]
    _, _, test_batches = __import__("data_loader").create_data_generators()
    class_names = [name for name, index in sorted(
        test_batches.class_indices.items(), key=lambda item: item[1]
    )]
    result = int(np.argmax(predictions))
    print("Scores:", {name: float(score) for name, score in zip(class_names, predictions)})
    print("Predicted class:", class_names[result])
    print(f"Score: {predictions[result]:.2%}")

if __name__ == "__main__":
    main()
