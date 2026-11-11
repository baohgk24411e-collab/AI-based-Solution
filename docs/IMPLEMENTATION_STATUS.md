# Trạng thái bàn giao ngày 11 tháng 11 năm 2026

## Kết quả đã có

| Hạng mục | Kết quả |
|---|---|
| PDF tải thành công | 20 |
| Công ty | 5 |
| Tổng trang PDF | 2.565 |
| Đoạn tìm kiếm | 4.930 |
| Trang khớp bộ lọc từ khóa | 389 |
| Đoạn ứng viên chưa xác nhận | 1.026 |
| Mẫu ưu tiên gán nhãn | 114 |
| Development / test | 10 / 10 báo cáo |
| PDF trùng SHA-256 | 0 |
| Kiểm tra ứng viên khớp trang nguồn | 1.026 / 1.026 |
| Trang ít văn bản cần xem lại | 37 |
| Kiểm thử phần mềm | 17 bài kiểm thử đạt |

Các con số lấy từ data/audit.json và lần chạy kiểm thử trong môi trường Python 3.12. Kiểm thử gồm 16 trường hợp logic và một luồng giao diện: mở app, đổi báo cáo, lọc đến danh sách rỗng. Giao diện cũng đã được mở trực tiếp trên trình duyệt và kiểm tra bằng ảnh. Đây không phải chỉ số đánh giá chất lượng mô hình.

## Phần chưa hoàn tất về thực nghiệm

- Chưa chạy Gemini thật vì môi trường không có API key. Tích hợp HTTP và kiểm tra đầu ra đã được viết, nhưng chưa được kiểm chứng bằng phản hồi dịch vụ thật.
- Chưa có nhãn chuẩn của người đọc hoặc xác nhận độc lập của hai người.
- Chưa đo accuracy, F1, extraction recall, thời gian tiết kiệm hoặc chi phí API.
- Chưa có kết luận greenwashing cho bất kỳ doanh nghiệp nào.

## Tài liệu

README.md hướng dẫn chạy; ANNOTATION_GUIDE.md quy định gán nhãn; DEMO_SCRIPT.md hướng dẫn trình bày; PROPOSAL_UPDATED.md là bản nội dung proposal cập nhật; SLIDES_UPDATED.md là nội dung 12 slide và lời dẫn. Hai PDF ban đầu của nhóm được giữ nguyên. Chưa tái dàn trang nội dung cập nhật thành PowerPoint hoặc PDF mới.

## Bước tiếp theo

1. Mở START.cmd, sau đó truy cập http://127.0.0.1:8501.
2. Nhập API key và model ID vào thanh bên, chạy thử 1–2 trang development.
3. Người trong nhóm gán nhãn, kiểm tra chéo và lưu đánh giá.
4. Chốt prompt và tiêu chí, sau đó chạy tập test. Báo cáo cả số mẫu đã xử lý và các trường hợp không chấm được.

Nếu API không được phép sử dụng, hệ thống vẫn hoạt động như công cụ tìm kiếm và rà soát bằng chứng. Khi đó cần đổi cách mô tả đề tài để không tuyên bố đã thực nghiệm LLM.
