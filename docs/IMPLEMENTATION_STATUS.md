# Cập nhật tích hợp LM Studio — 11/11/2026

## Các phần đã sửa

- `src/llm.py`: thêm LM Studio OpenAI-compatible adapter, JSON Schema cho trích xuất và đối chiếu, timeout, retry lỗi dịch vụ, cache tách theo provider/endpoint/model/prompt, ghi token và thời gian. Không tự chuyển sang cloud.
- Kiểm tra nguyên văn claim/trích dẫn; khi đối chiếu sai trích dẫn, cho một lần sửa có lưu metadata. Nếu vẫn sai thì không lưu assessment thành công.
- `run_llm.py`: xử lý toàn bộ 20 báo cáo, resume từng trang/claim, giữ lịch sử khi đổi cấu hình, lưu lỗi từng mục, xuất CSV/JSON/Markdown/HTML.
- `app.py`: mặc định LM Studio, Gemini tùy chọn; xem bảng tổng hợp và tải báo cáo. Giữ lịch sử các lần trích xuất trong giao diện.
- `prepare_review.py`: bỏ trạng thái cố định “chưa chạy vì thiếu API key”.
- `tests`: kiểm tra HTTP/schema/cache local, không cache đầu ra bị cắt, loại trích dẫn sai sau lần sửa, chuyển provider trong giao diện.

## Đầu ra thực nghiệm

Xem `../data/results/BAO_CAO_PHAN_TICH.md` và `../data/results/summary.csv` cho tiến độ và số liệu thực tế. Số trang LLM đọc được ghi riêng với tổng trang PDF. Lịch sử lỗi nằm trong `../data/batch_errors.json`.

Phạm vi vẫn là bao bì nhựa trong báo cáo PTBV. Chưa có OCR, tái dựng bảng hoặc đối chiếu nguồn bên ngoài. Nhãn AI chưa được người đọc thẩm định, không phải bằng chứng kết luận greenwashing; chưa có accuracy/F1.

Các tài liệu proposal và slide trước đây mô tả trạng thái bàn giao cũ. Dùng báo cáo thực nghiệm mới khi trình bày kết quả.
