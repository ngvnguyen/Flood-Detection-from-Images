# Chiến lược thiết kế giao diện Flood Detection

## 1. Tóm tắt định hướng

### Tầm nhìn

Biến mô hình phân loại ảnh ngập lụt thành một trải nghiệm web đơn giản, đáng tin cậy và dễ hiểu: người dùng tải một ảnh lên, nhận kết quả trong vài giây và biết rõ kết quả đó có ý nghĩa gì.

### Mục tiêu của giao diện

1. Rút ngắn đường đi từ mở trang đến kết quả còn **một luồng chính**.
2. Hiển thị kết quả theo cách người không chuyên vẫn hiểu được.
3. Không biến xác suất của mô hình thành một “cảnh báo chắc chắn”.
4. Tạo cảm giác sản phẩm phục vụ an toàn cộng đồng, không phải một trang demo kỹ thuật khô cứng.
5. Hoạt động tốt trên điện thoại, vì ảnh hiện trường thường được chụp và gửi từ thiết bị di động.

### Phạm vi MVP

Project hiện tại hỗ trợ:

- Phân loại một ảnh thành hai nhóm: **Flooding** và **No Flooding**.
- Nhận ảnh từ thư mục `evaluate/` qua script `predict.py`.
- Trả về điểm số cho các lớp và lớp được dự đoán.

Vì vậy, giao diện MVP nên tập trung vào **kiểm tra một ảnh tại một thời điểm**. Bản đồ trực tiếp, dự báo theo thời gian, mức độ ngập theo mét và cảnh báo khẩn cấp không nên xuất hiện như tính năng đã có nếu backend chưa cung cấp dữ liệu tương ứng.

---

## 2. Người dùng và nhu cầu

### Người dùng chính: người dân / người dùng phổ thông

- Muốn biết nhanh một bức ảnh có dấu hiệu ngập hay không.
- Không biết thuật ngữ machine learning.
- Có thể đang dùng điện thoại, mạng yếu hoặc ảnh có dung lượng lớn.
- Cần hướng dẫn rõ ràng hơn là nhiều số liệu kỹ thuật.

### Người dùng phụ: sinh viên, người đánh giá demo, nhà nghiên cứu

- Muốn xem điểm tin cậy và cách mô hình được đánh giá.
- Cần biết đây là kết quả hỗ trợ tham khảo, không phải kết luận thực địa.
- Có thể cần xem thêm thông tin dataset, accuracy, precision, F1 và confusion matrix ở khu vực riêng.

### Nguyên tắc UX

- **Một hành động chính:** tải ảnh lên và kiểm tra.
- **Kết quả trước, giải thích sau:** ưu tiên nhãn kết quả; điểm số và chi tiết mô hình nằm bên dưới.
- **Không gây hoảng sợ:** dùng ngôn ngữ trung tính, tránh màu đỏ toàn màn hình hoặc các từ như “nguy hiểm” khi hệ thống chỉ phân loại ảnh.
- **Minh bạch:** luôn cho biết đây là dự đoán từ ảnh và có thể sai.
- **Có đường lui:** cho phép đổi ảnh, thử lại và xem hướng dẫn ảnh phù hợp.

---

## 3. Kiến trúc thông tin

Thanh điều hướng tối giản:

1. **Kiểm tra ảnh** — màn hình mặc định và CTA chính.
2. **Cách hoạt động** — giải thích 3 bước, giới hạn và cách diễn giải kết quả.
3. **Đánh giá mô hình** — dành cho người muốn xem số liệu kỹ thuật.

Không nên đưa các mục sau vào MVP nếu chưa có backend:

- Bản đồ tình trạng ngập theo khu vực.
- Lịch sử dự đoán của nhiều người dùng.
- Đăng nhập và hồ sơ cá nhân.
- Gửi cảnh báo đến cơ quan chức năng.
- Dự báo mực nước hoặc thời gian ngập.

---

## 4. Luồng người dùng chính

```text
Mở trang
  -> Đọc giá trị chính và chọn ảnh
  -> Kéo thả / chọn ảnh từ thiết bị
  -> Xem ảnh xem trước
  -> Bấm "Kiểm tra ảnh"
  -> Trạng thái đang phân tích
  -> Xem kết quả Flooding hoặc No Flooding
  -> Đọc điểm tin cậy + lưu ý
  -> Thử ảnh khác hoặc xem cách hoạt động
```

### Hành vi cần thiết

- Chấp nhận JPG, JPEG và PNG; hiển thị giới hạn dung lượng rõ ràng.
- Có cả kéo-thả trên desktop và nút chọn file trên mobile.
- Hiển thị thumbnail trước khi gửi.
- Nút kiểm tra bị vô hiệu hóa khi chưa có ảnh.
- Cho phép thay ảnh mà không cần tải lại trang.
- Nếu ảnh lỗi, hiển thị nguyên nhân và cách khắc phục cụ thể.
- Nếu mô hình trả về điểm số thấp hoặc hai lớp gần nhau, hiển thị trạng thái “Kết quả chưa chắc chắn” thay vì cố tạo kết luận mạnh.

### Microcopy đề xuất

- Tiêu đề: **Kiểm tra ảnh có dấu hiệu ngập**
- Mô tả: **Tải lên một ảnh để mô hình phân tích nhanh. Kết quả chỉ mang tính tham khảo.**
- CTA: **Chọn ảnh để kiểm tra**
- Sau khi có ảnh: **Phân tích ảnh**
- Trạng thái chờ: **Đang phân tích ảnh…**
- Kết quả dương tính: **Có dấu hiệu ngập trong ảnh**
- Kết quả âm tính: **Chưa phát hiện dấu hiệu ngập rõ ràng**
- Lưu ý: **Không dùng kết quả này thay cho xác nhận tại hiện trường hoặc hướng dẫn khẩn cấp của cơ quan chức năng.**

---

## 5. Chiến lược cho từng màn hình

### 5.1. Trang kiểm tra ảnh

#### Bố cục desktop

- Header cao khoảng 64 px, logo/tên sản phẩm bên trái, điều hướng bên phải.
- Hero chia hai cột:
  - Cột trái: tiêu đề, mô tả ngắn, ba điểm tin cậy (nhanh, đơn giản, minh bạch).
  - Cột phải: vùng tải ảnh là điểm nhìn chính.
- Bên dưới: hàng “Cách hoạt động” gồm 3 bước.
- Cuối trang: lưu ý an toàn và liên kết đến phương pháp đánh giá.

#### Bố cục mobile

- Header gọn, điều hướng chuyển thành menu hoặc chỉ giữ liên kết cần thiết.
- Tiêu đề ngắn, không chiếm quá hai đến ba dòng.
- Vùng tải ảnh chiếm toàn bộ chiều rộng, tối thiểu 220 px chiều cao.
- CTA cố định theo ngữ cảnh ở cuối card, không dùng nút nổi che nội dung.

#### Vùng tải ảnh

Trạng thái rỗng cần có:

- Icon ảnh hoặc khung ngắm tối giản.
- Dòng chính: “Kéo ảnh vào đây hoặc chọn từ thiết bị”.
- Dòng phụ: “JPG, JPEG, PNG · tối đa 10 MB”.
- Nút chọn ảnh rõ ràng.

Sau khi chọn ảnh:

- Hiển thị preview với tỉ lệ ảnh được giữ nguyên.
- Có tên file, kích thước và nút “Đổi ảnh”.
- CTA “Phân tích ảnh” dùng màu nhấn.

### 5.2. Khu vực kết quả

Kết quả nên xuất hiện trong cùng trang, ngay dưới vùng tải ảnh để người dùng không mất ngữ cảnh.

Card kết quả gồm:

1. Nhãn kết quả lớn.
2. Chip trạng thái với màu có cả chữ, không chỉ dựa vào màu.
3. Điểm tin cậy dạng phần trăm và thanh tiến trình.
4. Ảnh đã phân tích ở kích thước vừa phải.
5. Một câu giải thích ngắn, không dùng thuật ngữ khó.
6. Lưu ý giới hạn.
7. Hai hành động: “Kiểm tra ảnh khác” và “Xem cách hoạt động”.

Không nên hiển thị điểm số với quá nhiều chữ số thập phân. Dùng phần trăm làm tròn, ví dụ `87%`, và đặt “điểm tin cậy của mô hình” ngay cạnh để tránh hiểu thành xác suất tuyệt đối.

### 5.3. Trang “Cách hoạt động”

Nội dung theo thứ tự:

1. Người dùng cung cấp một ảnh.
2. Ảnh được đưa về kích thước phù hợp với mô hình.
3. Mô hình so sánh ảnh với hai nhóm Flooding và No Flooding.
4. Hệ thống hiển thị lớp có điểm số cao hơn.

Thêm khối “Biết giới hạn”:

- Kết quả phụ thuộc vào chất lượng, góc chụp và bối cảnh ảnh.
- Ảnh mờ, quá tối hoặc không liên quan có thể cho kết quả sai.
- Kết quả không đo mực nước và không thay thế đánh giá thực địa.

### 5.4. Trang “Đánh giá mô hình”

Đây là khu vực dành cho người kỹ thuật, không đặt trên luồng chính. Hiển thị:

- Accuracy.
- Precision.
- F1 score.
- Confusion matrix.
- Mô tả ngắn về tập test và thời điểm đánh giá.

Chỉ hiển thị số liệu thực tế do backend cung cấp. Không điền số mẫu hoặc phần trăm giả để làm giao diện trông hoàn chỉnh.

---

## 6. Hệ thống hình ảnh và visual direction

### Concept

**“Clear signal after the storm”** — cảm giác đáng tin, bình tĩnh và có tính công nghệ; tránh mô tả thảm họa quá trực diện.

### Bảng màu đề xuất

- Nền chính: xanh đêm hơi xanh `#0B1726`.
- Bề mặt card: xanh slate `#13263A`.
- Nền sáng tùy chọn cho khu vực đọc: `#F4F8FB`.
- Màu nhấn hành động: cyan nước `#28C7D9`.
- Trạng thái Flooding: amber/cam `#F4A340`, đi kèm nhãn chữ.
- Trạng thái No Flooding: xanh lá dịu `#46B883`.
- Cảnh báo thông tin: `#F2C94C`.
- Chữ chính trên nền tối: `#F4F8FB`.
- Chữ phụ: `#A9BBCB`.

Màu cam chỉ nên dùng cho trạng thái và điểm cần chú ý, không dùng làm nền toàn trang. Trạng thái phải luôn được truyền tải bằng text và icon để đảm bảo accessibility.

### Typography

- Font sans-serif dễ đọc, hỗ trợ tiếng Việt tốt.
- Heading đậm vừa, ưu tiên độ rõ hơn phong cách sci-fi.
- Body tối thiểu 16 px trên mobile.
- Số phần trăm và metric dùng kiểu chữ có độ rộng ổn định để dễ quét.
- Duy trì tối đa ba cấp độ heading trong một màn hình.

### Hình ảnh

- Ưu tiên chính ảnh người dùng tải lên, không dùng ảnh stock gây cảm giác quảng cáo.
- Có khung preview rõ ràng, bo góc vừa phải, không dùng quá nhiều glassmorphism.
- Nếu cần ảnh minh họa hero, dùng ảnh đô thị sau mưa hoặc mặt nước trừu tượng với overlay tối; không dùng ảnh thảm họa gây giật gân.
- Icon nét đơn giản, nhất quán; không trộn emoji với icon hệ thống trong các trạng thái quan trọng.

### Layout và nhịp điệu

- Container tối đa khoảng 1120 px.
- Khoảng cách theo hệ 8 px: 8, 16, 24, 32, 48, 64.
- Card tải ảnh và card kết quả là hai khối thị giác chính; các phần giải thích nhẹ hơn.
- Bo góc 16 px cho card lớn, 10–12 px cho control.
- Bóng đổ nhẹ hoặc viền tương phản thấp; không dùng hiệu ứng nổi nặng.

---

## 7. Component và trạng thái bắt buộc

### Component cốt lõi

- `AppShell`
- `Header`
- `UploadDropzone`
- `ImagePreview`
- `AnalyzeButton`
- `AnalysisProgress`
- `PredictionResultCard`
- `ConfidenceBar`
- `InfoNotice`
- `HowItWorksSteps`
- `MetricCard`
- `ConfusionMatrixPanel`

### Trạng thái cần thiết kế trước khi code

1. Empty — chưa chọn ảnh.
2. Hover/focus — đang tương tác với vùng tải.
3. Selected — đã có preview.
4. Loading — đang gửi hoặc đang phân tích.
5. Success/Flooding.
6. Success/No Flooding.
7. Low confidence — điểm tin cậy thấp.
8. Invalid file — sai định dạng hoặc quá dung lượng.
9. Processing error — lỗi backend/model.
10. Offline/network timeout.
11. Reduced motion — người dùng yêu cầu giảm chuyển động.

Không dùng spinner vô hạn. Mọi trạng thái loading quá thời gian dự kiến cần có thông báo và hành động thử lại.

---

## 8. Responsive và accessibility

### Breakpoint thực dụng

- Mobile: dưới 640 px.
- Tablet: 640–1023 px.
- Desktop: từ 1024 px.

### Accessibility

- Tất cả nút và vùng tải có focus ring nhìn thấy được.
- Có label thật cho input file, không chỉ dùng placeholder.
- Kích thước vùng chạm tối thiểu khoảng 44 × 44 px.
- Tương phản chữ đạt WCAG AA.
- Không dùng màu đơn độc để phân biệt Flooding/No Flooding.
- Kết quả được thông báo bằng vùng live phù hợp cho screen reader.
- Có alt text mô tả ảnh preview hoặc đánh dấu ảnh người dùng nếu không cần mô tả nội dung.
- Hỗ trợ thao tác hoàn toàn bằng bàn phím.
- Animation chỉ dùng để báo trạng thái; tôn trọng `prefers-reduced-motion`.

---

## 9. Đo lường thành công

### Chỉ số UX cho MVP

- Tỷ lệ người dùng chọn được ảnh thành công.
- Tỷ lệ bấm “Phân tích ảnh” sau khi chọn ảnh.
- Thời gian từ chọn ảnh đến thấy kết quả.
- Tỷ lệ lỗi theo định dạng/dung lượng/network.
- Tỷ lệ người dùng bấm “Kiểm tra ảnh khác”.
- Tỷ lệ người dùng mở phần “Cách hoạt động”.

### Chỉ số chất lượng mô hình

Giữ tách biệt với chỉ số UX:

- Accuracy.
- Precision.
- F1 score.
- Confusion matrix.
- Phân bố kết quả có confidence thấp.

Không dùng tỷ lệ hoàn thành giao diện để suy luận mô hình chính xác hơn; hai nhóm chỉ số trả lời hai câu hỏi khác nhau.

---

## 10. Lộ trình triển khai

### Pha 1 — MVP demo

- Trang kiểm tra ảnh responsive.
- Upload, preview, validate file.
- Kết nối endpoint dự đoán thay cho việc phụ thuộc trực tiếp vào thư mục `evaluate/`.
- Card kết quả cho hai lớp.
- Loading, lỗi và trạng thái confidence thấp.
- Trang cách hoạt động và lưu ý giới hạn.

### Pha 2 — Tăng độ tin cậy

- Lịch sử cục bộ các ảnh vừa kiểm tra, nếu yêu cầu bảo mật cho phép.
- Hiển thị top-2 scores.
- Ghi nhận feedback “kết quả đúng/sai”.
- Trang đánh giá mô hình lấy metric động từ backend.
- Theo dõi latency và lỗi.

### Pha 3 — Mở rộng vận hành

- Batch upload nhiều ảnh.
- Gắn thời gian/vị trí do người dùng chủ động cung cấp.
- Dashboard theo khu vực chỉ khi có nguồn dữ liệu và chính sách riêng tư rõ ràng.
- Phân quyền cho cán bộ hoặc nhà nghiên cứu.

### Những điều không nên làm sớm

- Thêm bản đồ chỉ để làm dashboard trông “thông minh”.
- Hiển thị cảnh báo khẩn cấp dựa trên một ảnh đơn lẻ.
- Dùng gauge, biểu đồ và animation dày đặc cho một kết quả nhị phân.
- Ép người dùng đăng nhập trước khi thử demo.
- Hiển thị accuracy như một lời đảm bảo cho từng ảnh cụ thể.

---

## 11. Tiêu chí nghiệm thu giao diện

Một bản MVP đạt yêu cầu khi:

- Người dùng mới có thể hiểu hành động chính trong 5 giây đầu.
- Có thể chọn và phân tích ảnh bằng desktop lẫn mobile.
- Có preview trước khi phân tích.
- Kết quả thể hiện rõ lớp dự đoán, điểm tin cậy, ảnh nguồn và giới hạn.
- Tất cả trạng thái lỗi chính đều có hướng xử lý.
- Không có nội dung hứa hẹn vượt quá khả năng của mô hình hiện tại.
- Điều hướng bằng bàn phím và focus state hoạt động.
- Giao diện vẫn dễ đọc ở chiều rộng mobile.
- Số liệu kỹ thuật chỉ xuất hiện khi có dữ liệu thật từ hệ thống.

## 12. Quyết định cần chốt trước khi xây frontend

1. Backend sẽ cung cấp dự đoán qua API hay chạy model cùng process với web app?
2. Ngưỡng nào được xem là “confidence thấp”?
3. Giới hạn dung lượng và loại file chính thức là gì?
4. Ảnh người dùng có được lưu hay chỉ xử lý tạm thời?
5. Có cần hiển thị song ngữ Việt/Anh không?
6. Số liệu đánh giá model sẽ lấy từ file tĩnh hay endpoint động?

