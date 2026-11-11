# GreenClaim

Ứng dụng hỗ trợ đọc và kiểm chứng tuyên bố về bao bì nhựa trong báo cáo FMCG. Dự án có 20 PDF thật, dữ liệu theo trang, tìm kiếm BM25, pipeline Gemini API, kiểm tra tỷ lệ bằng Python và giao diện Streamlit tiếng Việt.

**Đọc trạng thái thực tế trước:** chế độ không API chỉ tạo đoạn ứng viên và tìm bằng chứng. Nó không kết luận greenwashing. Chưa có API key và chưa có nhãn người đọc độc lập, nên chưa có kết quả LLM thực nghiệm, accuracy hoặc F1.

## Mở trên máy hiện tại

1. Nhấp đúp `START.cmd`.
2. Giữ cửa sổ chương trình đang chạy.
3. Mở http://127.0.0.1:8501 trong trình duyệt.
4. Chọn báo cáo, vào tab **Đọc & đối chiếu** để xem đoạn ứng viên và trang nguồn.

`START.ps1` ưu tiên môi trường `.venv` hoạt động trong dự án. Trên máy hiện tại, thư viện cũng đã được cài riêng trong `.vendor` cho Python 3.12 đi kèm Codex để dự phòng. Máy khác cần cài độc lập theo hướng dẫn bên dưới. Chương trình chỉ lắng nghe trên máy bạn, không đưa dữ liệu lên một website công khai.

## Cài độc lập trên máy khác

Clone repository GitHub về máy mới, rồi mở terminal trong thư mục `greenclaim`. Cài Python 3.12 và bật tùy chọn thêm Python vào PATH. Không sao chép `.venv` hoặc `.vendor` giữa các máy. Chạy:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe launch.py
```

Không cần GPU. PDF, BM25 và phép tính chạy trên CPU. LLM chạy qua dịch vụ Gemini khi bạn chủ động bấm nút.

Sau khi cài xong, trên Windows có thể nhấp đúp `START.cmd` cho các lần sau. Nếu báo cổng 8501 đã được dùng, thử mở http://127.0.0.1:8501 để kiểm tra ứng dụng đang chạy.

API key không đi cùng repository: nhập lại key trong thanh bên trên máy mới. Nếu bản clone không có `data/raw_pdfs`, tải lại PDF từ danh sách nguồn bằng:

```powershell
.\.venv\Scripts\python.exe -m src.collect
```

Kiểm tra trạng thái tải của 20 báo cáo; URL nguồn có thể thay đổi. Dữ liệu đã xử lý đi kèm giúp đọc và tìm kiếm mà không cần chạy lại pipeline hay gọi API. Các kết quả LLM đã lưu trong `data/llm_claims` và `data/assessments` (nếu có) được giữ cùng dự án; cache và file tải lên cá nhân không đưa vào Git.

## Bật LLM

- Tạo API key trong Google AI Studio: https://aistudio.google.com/
- Nhập key vào ô mật khẩu trên thanh bên của ứng dụng. Không gửi key vào chat hoặc đưa vào Git.
- Nhập đúng model ID đang có trong tài khoản của bạn. Không cố định tên model vì quyền truy cập và model khả dụng có thể thay đổi.
- Tab **LLM**: chọn 1–3 trang, bấm **Trích claim bằng LLM**. Sau đó chọn claim ở tab 02 và bấm **Đối chiếu claim này bằng LLM**.
- Ứng dụng gửi đoạn văn bản tới Google, lưu phản hồi và token usage nhưng không lưu key. Các API call có thể có phí theo tài khoản. Chi phí chưa được đo trong lần bàn giao này.

Chạy theo lô trong một phiên PowerShell đã cấu hình `GEMINI_API_KEY` và `GEMINI_MODEL`:

```powershell
python run_llm.py --report nestle_2021 --stage extract --max-calls 2
python run_llm.py --report nestle_2021 --stage verify --max-calls 2
```

Mỗi lệnh có giới hạn số thao tác. Lệnh extract tiếp tục từ các trang chưa xử lý. Nó chỉ xét trang qua bộ lọc từ khóa, vì vậy cần kiểm tra độ bỏ sót. Lệnh verify mặc định bỏ qua claim đã có kết quả.

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `data/raw_pdfs/` | 20 PDF gốc tải từ nguồn chính thức |
| `data/sources.json` | Danh sách nguồn đã chọn, có URL và tập development/test |
| `data/manifest.csv` | Danh mục tải, số trang, SHA-256, URL sau chuyển hướng |
| `data/collection_attempts.json` | Nhật ký các nguồn ban đầu, gồm nguồn tải thất bại |
| `data/processed/` | Toàn văn theo trang và các đoạn tìm kiếm |
| `data/candidates.csv` | Đoạn ứng viên từ baseline, chưa gán nhãn |
| `data/annotation_queue.csv` | Mẫu ưu tiên để người đọc bắt đầu gán nhãn |
| `data/llm_claims/` | Claim đã qua API, khi có lần chạy |
| `data/assessments/` | Kết quả đối chiếu LLM, khi có lần chạy |
| `data/reviews/` | Lịch sử gán nhãn thủ công |
| `docs/` | Hướng dẫn gán nhãn, kịch bản demo, proposal và nội dung slide cập nhật |
| `tests/` | Kiểm thử logic và giao diện |

## Tái tạo dữ liệu và kiểm thử

Các lệnh dưới dùng môi trường đã cài `requirements.txt`:

```powershell
python -m src.collect
python -m src.pipeline
python -m src.evaluate
python -m unittest discover -s tests -v
```

Để dùng thư viện `.vendor` trên máy hiện tại, đặt `PYTHONPATH` thành thư mục `.vendor` và chạy bằng Python 3.12 trong `START.ps1`. Không dùng `.vendor` này với Python 3.14.

Crawler có hai chức năng: khám phá PDF trên một trang chỉ định và tải tập nguồn đã tuyển chọn. Nó chưa tự phân loại mọi PDF trên Internet:

```powershell
python -m src.collect --discover https://us.pg.com/sustainability-reports/
```

## Giới hạn cần trình bày với thầy

- Xử lý PDF có văn bản. Chưa OCR, chưa đọc biểu đồ ảnh và chưa tái dựng bảng nhiều cột thành bảng số chuẩn.
- `PDF page` đếm từ 1, có thể khác trang in. Trường `printed_page` chỉ là PDF page label, chưa chắc là số trang nhìn thấy trong ảnh.
- Baseline dùng từ khóa và chia câu nên có thể bỏ sót, lấy thừa hoặc cắt câu trong bảng. Đây là baseline để đo và cải thiện.
- BM25 tìm trong cùng báo cáo. Chưa đối chiếu liên niên hoặc với nguồn độc lập bên ngoài.
- Trích dẫn khớp văn bản chỉ chứng minh nguồn có câu đó, không chứng minh suy luận của LLM đúng.
- Kiểm tra số liệu nhận số do người đọc nhập và xác nhận tính tương thích, chưa tự rút số từ PDF.
- Độ chính xác LLM và chi phí API chưa được đo. Nhãn AI, ví dụ trợ lý và kiểm thử giả lập không được coi là nhãn chuẩn của người đọc.
- Giao diện phù hợp demo nội bộ trên máy cá nhân. Chưa có đăng nhập hay cơ chế nhiều người cùng ghi dữ liệu đồng thời.

## Tài liệu kỹ thuật

- Gemini API key: https://ai.google.dev/gemini-api/docs/api-key
- Generate content REST: https://ai.google.dev/api/generate-content
- Streamlit: https://docs.streamlit.io/
- pypdf: https://pypdf.readthedocs.io/

PDF gốc thuộc bản quyền đơn vị phát hành; không thuộc giấy phép của mã nguồn. Bản bàn giao chuyển máy gồm 20 PDF và danh sách URL nguồn để phục vụ nghiên cứu môn học.
