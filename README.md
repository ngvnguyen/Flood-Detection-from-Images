# Flood Detection - Python files

## Cấu trúc thư mục

```text
flood_detection_python/
├── config.py
├── data_loader.py
├── model.py
├── train.py
├── evaluate.py
├── predict.py
├── requirements.txt
├── data/
│   ├── train/
│   │   ├── Flooding/
│   │   └── No Flooding/
│   ├── valid/
│   │   ├── Flooding/
│   │   └── No Flooding/
│   └── test/
│       ├── Flooding/
│       └── No Flooding/
└── evaluate/
    └── 8.jpg
```

Tên thư mục lớp phải nhất quán giữa `train`, `valid`, `test`. Keras tự gán chỉ số lớp theo thứ tự alphabet; chương trình đánh giá/dự đoán sẽ đọc đúng thứ tự này từ dữ liệu.

## Cài thư viện

```bash
python -m pip install -r requirements.txt
```

## Phân loại ảnh

Đặt dataset vào raw_data, chạy ```python split.py``` để phân loại vào thư mục data.

## Chạy theo thứ tự

1. Huấn luyện và lưu mô hình:

   ```bash
   python train.py
   ```

2. Đánh giá trên tập test:

   ```bash
   python evaluate.py
   ```

3. Dự đoán ảnh `8.jpg` trong thư mục `evaluate`:

   ```bash
   python predict.py 8.jpg
   ```

Lưu ý: lần chạy đầu tiên, TensorFlow có thể tải trọng số ImageNet của MobileNet. Mô hình lưu ở `fine_tuned_flood_detection_model.keras`.

## Chạy giao diện web demo

Giao diện FloodLens nằm ở `index.html`, `styles.css` và `app.js`. Đây là giao diện responsive cho luồng chọn ảnh, xem trước, trạng thái phân tích và hiển thị kết quả.

Cài dependency và chạy server Flask để giao diện gọi model thật:

```bash
python -m pip install -r requirements.txt
python server.py
```

Mở `http://127.0.0.1:5000`. Endpoint `POST /api/predict` nhận field `image`, nạp `fine_tuned_flood_detection_model.keras` và trả về lớp dự đoán cùng điểm số. Không mở `index.html` trực tiếp bằng `file://`, vì khi đó trình duyệt không có API `/api/predict`.
