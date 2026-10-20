"""Cấu hình đường dẫn và tham số cho Flood Detection."""
import os
DATA_DIR = "data"
TRAIN_PATH = os.path.join(DATA_DIR, "train")
VALID_PATH = os.path.join(DATA_DIR, "valid")
TEST_PATH = os.path.join(DATA_DIR, "test")
EVALUATE_DIR = "evaluate"
MODEL_PATH = "fine_tuned_flood_detection_model.keras"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 10
EPOCHS = 10
LEARNING_RATE = 0.0001

# Thứ tự lớp phụ thuộc vào tên thư mục được Keras sắp xếp alphabet.
# Nếu thư mục là flooding/ và no_flooding/, class_indices thường là
# flooding=0, no_flooding=1.
