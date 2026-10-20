
import random
import shutil
from pathlib import Path

# Đường dẫn thư mục
RAW_DIR = Path("raw_data")
DATA_DIR = Path("data")

# Tỷ lệ chia dữ liệu
TRAIN_RATIO = 0.70
VALID_RATIO = 0.15
TEST_RATIO = 0.15

# Đảm bảo kết quả chia có thể tái lập
random.seed(42)

# Các định dạng ảnh được hỗ trợ
IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".webp"
}

CLASSES = ["flooding", "normal"]

# Tạo thư mục train, valid, test
for split in ["train", "valid", "test"]:
    for class_name in CLASSES:
        (DATA_DIR / split / class_name).mkdir(
            parents=True, exist_ok=True
        )

# Chia ảnh từng lớp
for class_name in CLASSES:
    source_dir = RAW_DIR / class_name

    if not source_dir.exists():
        raise FileNotFoundError(
            f"Không tìm thấy thư mục: {source_dir}"
        )

    images = [
        p for p in source_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_RATIO)
    val_end = train_end + int(total * VALID_RATIO)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    splits = {
        "train": train_images,
        "valid": val_images,
        "test": test_images,
    }

    print(f"\nLớp: {class_name} | Tổng: {total} ảnh")

    for split, split_images in splits.items():
        dest_dir = DATA_DIR / split / class_name

        for image_path in split_images:
            shutil.copy2(
                image_path,
                dest_dir / image_path.name
            )

        print(f"  {split}: {len(split_images)} ảnh")

print("\nĐã chia dữ liệu thành công!")
