"""Tạo các batch ảnh train/validation/test."""
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config import TRAIN_PATH, VALID_PATH, TEST_PATH, IMAGE_SIZE, BATCH_SIZE

def create_data_generators():
    preprocessing = tf.keras.applications.mobilenet.preprocess_input
    train_batches = ImageDataGenerator(
        preprocessing_function=preprocessing
    ).flow_from_directory(
        directory=TRAIN_PATH, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE
    )
    valid_batches = ImageDataGenerator(
        preprocessing_function=preprocessing
    ).flow_from_directory(
        directory=VALID_PATH, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE
    )
    test_batches = ImageDataGenerator(
        preprocessing_function=preprocessing
    ).flow_from_directory(
        directory=TEST_PATH, target_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
        shuffle=False
    )
    return train_batches, valid_batches, test_batches
