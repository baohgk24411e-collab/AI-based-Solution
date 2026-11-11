# Kịch bản demo khoảng 5 phút

## 1 Giới thiệu vấn đề

“Nhóm xây dựng hệ thống hỗ trợ kiểm chứng các tuyên bố về bao bì nhựa trong báo cáo FMCG. Hệ thống giúp người đọc tìm và đối chiếu bằng chứng, chưa đưa ra kết luận pháp lý hoặc khẳng định doanh nghiệp greenwashing.”

## 2 Dữ liệu đã thu thập

Mở tab Dữ liệu. Chỉ ra 20 báo cáo, 5 công ty, số trang thực tế và danh mục nguồn. Giải thích rằng P&G và Reckitt thay nguồn không tải được. Danh mục có URL, năm, mã băm để truy vết.

## 3 Đọc một claim và tìm bằng chứng

Chọn một báo cáo Coca-Cola hoặc Nestlé, vào Đọc & đối chiếu. Lọc “recycled” hoặc “packaging”. Chọn một đoạn ngắn rõ nghĩa. Chỉ ra số trang PDF, toàn văn trang, danh sách BM25 và nút mở nguồn. Nếu đoạn tìm về chỉ lặp lại claim, chỉ ra cảnh báo đó.

“Đây là baseline tìm kiếm, chưa phải kết quả LLM. Nhóm giữ lại để so sánh và có thể demo khi không có mạng hoặc API.”

## 4 Phần lõi LLM

Nếu đã có API: chọn 1–2 trang, trích claim, xem các trường có cấu trúc. Sau đó chọn claim và đối chiếu. Hiển thị nhãn, lý do, trích dẫn và số token. Không dùng một lần chạy để khẳng định độ chính xác toàn hệ thống.

Nếu chưa có API: trình bày prompt trong src/llm.py và giao diện đã tích hợp. Nói rõ “phần gọi API chưa chạy thực nghiệm”, không gọi baseline là LLM.

## 5 Kiểm tra phép tính

Dùng số thật đã đọc đầy đủ điều kiện; hoặc ghi rõ ví dụ giả lập trong lời nói: 2.500 tấn / 10.000 tấn = 25%, nhưng 2.500 / 4.000 = 62,5%. Đây là hai mẫu số khác nhau. Đừng trình bày con số này như dữ liệu của doanh nghiệp đang mở.

## 6 Kết quả và bước còn lại

Mở tab Đánh giá. Trình bày đúng trạng thái hiện có. Chưa có nhãn người đọc và API run thì accuracy/F1 chưa xác định. Bước còn lại là gán nhãn độc lập, chốt prompt trên development và chạy test.

## Trả lời câu hỏi của thầy

- Crawl gì: tải PDF báo cáo từ website chính thức cùng metadata, kiểm tra PDF và phát hiện trùng bằng SHA-256.
- Lõi gì: LLM trích claim có cấu trúc và đối chiếu bằng chứng BM25 theo kỳ, vật liệu, phạm vi và nội dung. Python kiểm tra số học.
- Xuất gì: claim, nhãn, lý do, đoạn bằng chứng, trang nguồn và kết quả tính lại khi có dữ liệu tương thích.
- Vì sao cần LLM: hiểu khác biệt giữa mục tiêu, kết quả, phạm vi và cách diễn đạt; từ khóa chỉ giúp tìm ứng viên.
- Máy yếu thì sao: các tác vụ nhẹ chạy local, mô hình chạy qua API. Chưa cần fine-tune.
- Vì sao chưa gọi là phát hiện greenwashing chắc chắn: báo cáo doanh nghiệp là nguồn tự công bố, chưa có xác minh thực địa/nguồn độc lập.
