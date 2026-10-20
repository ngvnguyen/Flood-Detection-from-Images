"""Đánh giá mô hình bằng tập test và vẽ confusion matrix."""
import itertools
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_score, f1_score, accuracy_score
from config import MODEL_PATH
from data_loader import create_data_generators

def plot_confusion_matrix(cm, classes, title="Confusion matrix"):
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
    plt.ylabel("True label")
    plt.xlabel("Predicted label")

def main():
    _, _, test_batches = create_data_generators()
    import tensorflow as tf
    model = tf.keras.models.load_model(MODEL_PATH)
    test_labels = test_batches.classes
    predictions = model.predict(test_batches, steps=len(test_batches), verbose=0)
    predicted_labels = predictions.argmax(axis=1)

    precision = precision_score(test_labels, predicted_labels, zero_division=0)
    f1 = f1_score(test_labels, predicted_labels, zero_division=0)
    accuracy = accuracy_score(test_labels, predicted_labels)
    print("Class indices:", test_batches.class_indices)
    print("Precision:", precision)
    print("F1 Score:", f1)
    print("Accuracy:", accuracy)

    # Dùng tên lớp theo đúng class_indices của thư mục dữ liệu.
    class_names = [name for name, index in sorted(
        test_batches.class_indices.items(), key=lambda item: item[1]
    )]
    cm = confusion_matrix(test_labels, predicted_labels)
    plot_confusion_matrix(cm, class_names, title="Confusion Matrix")
    plt.show()

if __name__ == "__main__":
    main()
