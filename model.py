"""Xây dựng mô hình phân loại ngập lụt dựa trên MobileNet."""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from config import LEARNING_RATE

def build_model():
    mobile = tf.keras.applications.mobilenet.MobileNet(
        weights="imagenet", include_top=False
    )
    x = mobile.layers[-12].output
    x = keras.layers.GlobalAveragePooling2D()(x)
    x = keras.layers.Dropout(0.2)(x)
    output = Dense(units=2, activation="sigmoid")(x)
    model = Model(inputs=mobile.input, outputs=output)

    # Giữ nguyên cách đóng băng lớp của notebook gốc.
    for layer in model.layers[:-23]:
        layer.trainable = False

    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
