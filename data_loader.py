"""Tạo các batch ảnh train/validation/test kèm Data Augmentation."""
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config import TRAIN_PATH, VALID_PATH, TEST_PATH, IMAGE_SIZE, BATCH_SIZE

def create_data_generators():
    preprocessing = tf.keras.applications.mobilenet.preprocess_input

    # Tăng cường dữ liệu (Data Augmentation) cho tập train để tránh học vẹt đặc trưng màu trời/đường
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocessing,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode="nearest"
    )

    # Tập validation và test giữ nguyên ảnh gốc, chỉ tiền xử lý chuẩn hóa
    eval_datagen = ImageDataGenerator(
        preprocessing_function=preprocessing
    )

    train_batches = train_datagen.flow_from_directory(
        directory=TRAIN_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=True
    )

    valid_batches = eval_datagen.flow_from_directory(
        directory=VALID_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False
    )

    test_batches = eval_datagen.flow_from_directory(
        directory=TEST_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        shuffle=False
    )

    return train_batches, valid_batches, test_batches
