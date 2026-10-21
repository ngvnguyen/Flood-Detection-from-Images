"""Đánh giá mô hình bằng tập test và vẽ confusion matrix."""
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, precision_score, f1_score, accuracy_score
import tensorflow as tf
from config import MODEL_PATH
from data_loader import create_data_generators

def plot_confusion_matrix(cm, classes, title="Confusion Matrix"):
    plt.figure(figsize=(6, 5))
    plt.imshow(cm, interpolation="nearest", cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.0 if cm.size else 0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j, i, cm[i, j], horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black"
        )
    plt.tight_layout()
    plt.ylabel("Nhãn thực tế (True label)")
    plt.xlabel("Nhãn dự đoán (Predicted label)")

def main():
    _, _, test_batches = create_data_generators()
    model = tf.keras.models.load_model(MODEL_PATH)
    test_labels = test_batches.classes
    
    # Dự đoán trên toàn bộ tập test
    predictions = model.predict(test_batches, steps=len(test_batches), verbose=1)
    predicted_labels = predictions.argmax(axis=1)

    class_names = [name for name, _ in sorted(
        test_batches.class_indices.items(), key=lambda item: item[1]
    )]

    precision = precision_score(test_labels, predicted_labels, average="weighted", zero_division=0)
    f1 = f1_score(test_labels, predicted_labels, average="weighted", zero_division=0)
    accuracy = accuracy_score(test_labels, predicted_labels)

    print("=" * 50)
    print("Class mapping:", test_batches.class_indices)
    print(f"Accuracy:  {accuracy:.4f} ({accuracy:.2%})")
    print(f"Precision: {precision:.4f} ({precision:.2%})")
    print(f"F1-Score:  {f1:.4f}")
    print("=" * 50)
    print("\nChi tiết đánh giá từng lớp (Classification Report):")
    print(classification_report(test_labels, predicted_labels, target_names=class_names, zero_division=0))

    cm = confusion_matrix(test_labels, predicted_labels)
    plot_confusion_matrix(cm, class_names, title="Ma trận nhầm lẫn (Confusion Matrix)")
    plt.show()

if __name__ == "__main__":
    main()
