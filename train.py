"""Huấn luyện và lưu mô hình cùng thông tin phân lớp."""
import json
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from config import EPOCHS, MODEL_PATH, CLASSES_PATH
from data_loader import create_data_generators
from model import build_model

def main():
    train_batches, valid_batches, _ = create_data_generators()
    
    # Lưu bảng ánh xạ lớp (class_indices) để dùng cho predict và server mà không sợ lệch thứ tự alphabet
    class_indices = train_batches.class_indices
    with open(CLASSES_PATH, "w", encoding="utf-8") as f:
        json.dump(class_indices, f, indent=2)
    print(f"Bảng ánh xạ nhãn được lưu tại {CLASSES_PATH}: {class_indices}")

    model = build_model()
    model.summary()

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        ),
        ModelCheckpoint(
            MODEL_PATH,
            monitor="val_loss",
            save_best_only=True,
            verbose=1
        )
    ]

    model.fit(
        x=train_batches,
        steps_per_epoch=len(train_batches),
        validation_data=valid_batches,
        validation_steps=len(valid_batches),
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    print(f"Hoàn thành huấn luyện! Mô hình tốt nhất đã được lưu tại: {MODEL_PATH}")

if __name__ == "__main__":
    main()
