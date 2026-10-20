"""Huấn luyện và lưu mô hình."""
from config import EPOCHS, MODEL_PATH
from data_loader import create_data_generators
from model import build_model

def main():
    train_batches, valid_batches, _ = create_data_generators()
    model = build_model()
    model.summary()
    model.fit(
        x=train_batches,
        steps_per_epoch=len(train_batches),
        validation_data=valid_batches,
        validation_steps=len(valid_batches),
        epochs=EPOCHS,
        verbose=2,
    )
    model.save(MODEL_PATH)
    print(f"Đã lưu mô hình tại: {MODEL_PATH}")

if __name__ == "__main__":
    main()
