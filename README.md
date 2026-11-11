# GreenClaim

Ứng dụng hỗ trợ đọc và đối chiếu tuyên bố về **bao bì nhựa** trong 20 báo cáo PTBV của 5 doanh nghiệp FMCG. Hỗ trợ LM Studio trên PC và Gemini tùy chọn. Không phải công cụ chấm điểm toàn bộ ESG hay kết luận doanh nghiệp greenwashing.

## Chạy trên PC với LM Studio

1. Bật local server LM Studio ở http://127.0.0.1:1234.
2. Nạp model `qwen2.5-7b-instruct`, context 16.384 token.
3. Nhấp đúp `START.cmd`, mở http://127.0.0.1:8501 và chọn `lmstudio`. Không cần API key.

```powershell
lms load qwen2.5-7b-instruct --context-length 16384 -y
.\.venv\Scripts\python.exe -X utf8 run_llm.py --report all --stage all
```

Chạy lại cùng lệnh để tiếp tục. Mỗi trang/claim được lưu ngay; lỗi từng mục nằm trong `data/batch_errors.json`. Không chạy hai batch cùng lúc. Cache phân biệt provider, endpoint, model, prompt và nội dung. Khi thay cấu hình trích xuất, dữ liệu cũ được giữ trong `data/run_archive`.

Tùy chọn: `--report pg_2021`, `--stage extract|verify|all|export`, `--max-calls 2`, `--model ID`, `--base-url URL`. `--max-calls` giới hạn thao tác; một thao tác đối chiếu có thể gọi thêm một lần để sửa trích dẫn lỗi. Không đặt giới hạn sẽ xử lý toàn bộ phần còn lại.

Biến môi trường: `LM_STUDIO_BASE_URL`, `LM_STUDIO_MODEL`. Gemini chỉ được gọi khi chọn `--provider gemini` và cấu hình `GEMINI_API_KEY`, `GEMINI_MODEL`; văn bản khi đó gửi tới Google. Không lưu key vào Git.

## Kết quả

- `data/results/BAO_CAO_PHAN_TICH.md`: báo cáo tiếng Việt, độ phủ và ví dụ dẫn trang.
- `data/results/summary.csv`: bảng tổng hợp 20 báo cáo, mở bằng Excel.
- `data/results/claims_and_assessments.csv` và `.json`: claim, nhãn, lý do, trích dẫn.
- `data/llm_claims`: trích xuất, mục bị loại, metadata model/token/thời gian.
- `data/assessments`: đối chiếu đã qua kiểm tra trích dẫn.
- `data/batch_errors.json`: lịch sử lỗi, có thể gồm lỗi đã sửa ở lần sau; độ phủ hiện tại nằm trong bảng tổng hợp.

Tab Dữ liệu cho tải báo cáo tổng hợp. Tab Đọc & đối chiếu hiển thị trang nguồn, bằng chứng BM25 và gán nhãn. Tab LLM chạy từng trang/claim. Tab Kiểm tra số tính lại tỷ lệ từ dữ liệu người đọc đã xác nhận.

## Cài trên máy khác

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe launch.py
```

Không sao chép `.venv` giữa máy. LM Studio và model cài riêng. PDF/BM25 chạy CPU; LLM dùng phần cứng do LM Studio cấu hình. Nếu thiếu PDF, chạy `python -m src.collect` để tải từ danh sách nguồn.

## Phương pháp và giới hạn

Toàn văn các trang PDF được lập chỉ mục BM25. LLM trích claim trên trang qua bộ lọc bao bì/tái chế; trang ngoài bộ lọc chưa được LLM đọc. Đối chiếu dùng 5 đoạn tìm về trong cùng báo cáo. Đây là phân tích cả bộ theo phạm vi đề tài, không phải đọc bằng LLM mọi nội dung ESG.

Trích dẫn không khớp nguồn bị loại. Khớp nguyên văn chỉ xác nhận vị trí, không chứng minh suy luận đúng. Mô hình vẫn có thể hiểu sai kỳ đo, phạm vi hoặc mục tiêu; mọi nhãn cần người đọc kiểm tra. `supported` là hỗ trợ trong tài liệu, không xác minh độc lập.

Chưa OCR hay tái dựng bảng nhiều cột. PDF page bắt đầu từ 1, có thể khác trang in. Bộ lọc có thể bỏ sót claim. Chưa có nhãn chuẩn nên chưa công bố accuracy/F1 hay recall. Kiểm thử phần mềm không phải đánh giá chất lượng mô hình.

## Kiểm tra và tái tạo

```powershell
.\.venv\Scripts\python.exe -m src.pipeline
.\.venv\Scripts\python.exe prepare_review.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m src.evaluate
.\.venv\Scripts\python.exe run_llm.py --stage export
```

`data/manifest.csv` lưu URL, số trang và SHA-256. `docs/ANNOTATION_GUIDE.md` hướng dẫn gán nhãn. Proposal/slide cũ là tài liệu lịch sử; xem báo cáo kết quả mới cho trạng thái hiện tại.

Giao thức: [LM Studio OpenAI compatibility](https://lmstudio.ai/docs/developer/openai-compat). PDF thuộc quyền đơn vị phát hành, được giữ để nghiên cứu môn học.
