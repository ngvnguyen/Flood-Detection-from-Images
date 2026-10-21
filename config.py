"""Cấu hình đường dẫn và tham số cho Flood Detection."""
import os

DATA_DIR = "data"
TRAIN_PATH = os.path.join(DATA_DIR, "train")
VALID_PATH = os.path.join(DATA_DIR, "valid")
TEST_PATH = os.path.join(DATA_DIR, "test")
EVALUATE_DIR = "evaluate"
MODEL_PATH = "fine_tuned_flood_detection_model.keras"
CLASSES_PATH = "classes.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 15
LEARNING_RATE = 0.0001
