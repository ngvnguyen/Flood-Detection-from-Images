"""Xây dựng mô hình phân loại ngập lụt dựa trên MobileNet."""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from config import LEARNING_RATE, IMAGE_SIZE

def build_model():
    input_shape = (IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
    base_model = tf.keras.applications.mobilenet.MobileNet(
        weights="imagenet",
        include_top=False,
        input_shape=input_shape
    )

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation="relu")(x)
    x = Dropout(0.3)(x)
    # Dùng softmax cho bài toán phân loại đa lớp/2 lớp dạng categorical để tổng xác suất = 1
    output = Dense(units=2, activation="softmax")(x)

    model = Model(inputs=base_model.input, outputs=output)

    # Đóng băng các tầng trích xuất đặc trưng cơ bản ban đầu,
    # chỉ mở khóa 20 tầng cuối cùng để tinh chỉnh (fine-tune) đặc trưng ngập lụt
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    for layer in base_model.layers[-20:]:
        layer.trainable = True

    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
