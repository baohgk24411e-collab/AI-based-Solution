# Giới Hạn Kỹ Thuật & Ranh Giới Của Hệ Thống (Pipeline Limitations)

## 1. Hạn Chế Trong Trích Xuất Văn Bản PDF & Cấu Trúc Bảng
* **Chỉ xử lý luồng văn bản gốc (Chưa có OCR):** Hệ thống sử dụng `pypdf` để đọc text layer. Các trang báo cáo được xuất dưới dạng ảnh chụp, infographic hoặc biểu đồ chứa chữ mà không có lớp văn bản (text layer) sẽ không đọc được nếu không tích hợp thêm bộ nhận diện ký tự quang học (OCR như Tesseract/PaddleOCR).
* **Bảng nhiều cột và mất cấu trúc dòng:** Báo cáo phát triển bền vững thường trình bày số liệu trong bảng nhiều cột phức tạp. Khi trích xuất tuyến tính thành chuỗi văn bản, các cột và dòng có thể bị trộn thứ tự, khiến LLM đôi khi gán nhầm số liệu của năm/cột kế cận vào câu tuyên bố.
* **Số trang vật lý (PDF Page) khác số trang in:** Chỉ số trang PDF đếm từ 1 thường lệch so với số trang in hiển thị trên góc tài liệu do bao gồm trang bìa, mục lục hoặc số La Mã.

## 2. Giới Hạn Trong Truy Xuất Bằng Chứng (BM25 Lexical Scope)
* **Chỉ đối chiếu trong nội bộ cùng một báo cáo (Intra-report):** Hệ thống tìm kiếm BM25 hiện tại chỉ quét dữ liệu trong cùng một `report_id`. Chưa tự động liên kết đối chiếu chéo liên niên (ví dụ: so sánh lời hứa ở báo cáo 2021 với kết quả thực tế ở báo cáo 2024).
* **Truy xuất từ khóa vs Ngữ nghĩa sâu:** BM25 dựa trên tần suất từ khóa trùng khớp. Nếu phần bằng chứng nằm ở một trang dùng từ ngữ diễn giải hoàn toàn khác (paraphrase), độ phủ tìm kiếm (recall) có thể thấp hơn so với tìm kiếm vector ngữ nghĩa (dense embeddings).

## 3. Hiện Tượng Hallucination Số Liệu Của LLM Cục Bộ
* **Nhầm lẫn ô bảng lân cận (Context Cell Confusion):** Khi trích xuất các trường số liệu (`value`, `unit`, `target_year`), mô hình 7B cục bộ (Qwen 2.5 7B) thỉnh thoảng nhặt nhầm tỷ lệ tiến độ hiện tại (ví dụ: 90%) từ dòng kế bên thay vì tỷ lệ mục tiêu của câu (100%).
* **Tự suy diễn từ ngữ định tính thành số (Implicit Deduction):** Các cụm từ như *"halve our virgin plastics"* (giảm một nửa nhựa nguyên sinh) đôi khi được LLM tự quy đổi thành `50%` dù con số `50` không xuất hiện nguyên văn trong câu.
* **Quy đổi đơn vị quy mô (Scale Expansion):** Các cụm từ như *"3 million metric tons"* được LLM tự mở rộng thành `3000000` thay vì giữ nguyên giá trị số `3` và đơn vị `million metric tons`.
* **Độ dài ngữ cảnh (Context Length Limit):** Các trang PDF quá dày đặc văn bản bảng biểu (như trang 201 của `danone_2023` dài 6.491 ký tự) có thể vượt ngưỡng bộ nhớ sinh JSON của mô hình cục bộ 7B dẫn đến lỗi sinh dở dang.

## 4. Phạm Vi Kết Luận Greenwashing
* **Xác thực tài liệu (Documentary Support) ≠ Kiểm toán thực địa:** Nhãn `supported` chỉ xác nhận rằng *bên trong báo cáo có dẫn chứng và số liệu hỗ trợ cho tuyên bố đó*. Hệ thống không thay thế cho việc kiểm toán độc lập chuỗi cung ứng hoặc kiểm chứng dữ liệu thực tế bên ngoài báo cáo doanh nghiệp.
