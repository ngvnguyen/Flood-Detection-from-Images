"""Web server for FloodLens predictions."""
from __future__ import annotations

import io
import os
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request, send_from_directory
from PIL import UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "fine_tuned_flood_detection_model.keras"
IMAGE_SIZE = (224, 224)
MAX_FILE_SIZE = 10 * 1024 * 1024
CLASS_NAMES = ("flooding", "normal")

app = Flask(__name__, static_folder=str(ROOT), static_url_path="")
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE
model = None


def get_model() -> Any:
    global model
    if model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Không tìm thấy model: {MODEL_PATH.name}")
        model = tf.keras.models.load_model(MODEL_PATH)
    return model


def predict_image(image_bytes: bytes) -> dict[str, Any]:
    try:
        image = tf.keras.utils.load_img(
            io.BytesIO(image_bytes), target_size=IMAGE_SIZE, color_mode="rgb"
        )
    except (UnidentifiedImageError, OSError, ValueError) as error:
        raise ValueError("File được gửi lên không phải ảnh hợp lệ.") from error

    array = tf.keras.utils.img_to_array(image)
    array = np.expand_dims(array, axis=0)
    array = tf.keras.applications.mobilenet.preprocess_input(array)
    raw_scores = np.asarray(get_model().predict(array, verbose=0)[0], dtype=float)
    if raw_scores.size != len(CLASS_NAMES) or not np.all(np.isfinite(raw_scores)):
        raise RuntimeError("Model trả về kết quả không hợp lệ.")

    # The current model has a two-unit sigmoid output. Normalize its scores
    # so the UI presents the relative confidence for the two known classes.
    scores = raw_scores / raw_scores.sum() if raw_scores.sum() > 0 else raw_scores
    result_index = int(np.argmax(scores))
    display_names = {"flooding": "Flooding", "normal": "No Flooding"}
    return {
        "label": CLASS_NAMES[result_index],
        "display_label": display_names[CLASS_NAMES[result_index]],
        "confidence": round(float(scores[result_index]), 4),
        "scores": {
            display_names[name]: round(float(score), 4)
            for name, score in zip(CLASS_NAMES, scores)
        },
    }


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(_error: RequestEntityTooLarge):
    return jsonify({"error": "Ảnh quá lớn. Vui lòng chọn ảnh có dung lượng tối đa 10 MB."}), 413


@app.get("/")
def index():
    return send_from_directory(ROOT, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "model": MODEL_PATH.name, "model_exists": MODEL_PATH.exists()})


@app.post("/api/predict")
def predict():
    uploaded_file = request.files.get("image")
    if uploaded_file is None or not uploaded_file.filename:
        return jsonify({"error": "Chưa nhận được file ảnh."}), 400

    try:
        result = predict_image(uploaded_file.read())
    except FileNotFoundError as error:
        return jsonify({"error": str(error)}), 503
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({"error": "Không thể phân tích ảnh lúc này. Vui lòng thử lại."}), 500
    return jsonify(result)


if __name__ == "__main__":
    app.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", "5000")), debug=False)
