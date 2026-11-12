# Kiến Trúc Hệ Thống & Quy Trình Xử Lý AI (Pipeline)

```
+-----------------------------------------------------------------------------------+
|                            KIẾN TRÚC AI GREENCLAIM                                |
+-----------------------------------------------------------------------------------+
                                         │
 1. THU THẬP DỮ LIỆU                     ▼
    [ 20 Báo cáo PDF Doanh nghiệp ] ──> [ Trình trích xuất pypdf ]
                                         │
 2. TIỀN XỬ LÝ VĂN BẢN                   ▼
    [ Đánh số trang vật lý ] ──> [ Chia đoạn (2.500 ký tự, gối đầu 400 ký tự) ]
                                         │
 3. LỌC TỪ KHÓA SƠ BỘ                    ▼
    [ Từ khóa Bao bì & Tái chế ] ──> [ Lọc ra 389 Trang liên quan ]
                                         │
 4. TRÍCH XUẤT CLAIM BẰNG LLM            ▼
    [ LM Studio Cục bộ (Qwen 2.5 7B) / Gemini ] ──> Ràng buộc JSON Schema nghiêm ngặt
                                         │
                                         ├──> [ Kiểm tra trích dẫn nguyên văn: 100% Grounded ]
                                         └──> [ Trích xuất 631 Claims kèm Metadata ]
                                         │
 5. TRUY XUẤT BẰNG CHỨNG (RETRIEVAL)     ▼
    [ Chỉ mục đảo BM25 toàn báo cáo ] ──> [ Top-K Đoạn ứng viên cho mỗi Claim ]
                                         │
 6. THẨM ĐỊNH & KIỂM ĐỊNH ĐA BƯỚC        ▼
    [ Agent Đối chiếu & Giải thích LLM ] ──> [ Xác thực khớp chuỗi nguyên văn ]
                                         │
                                         ├──> Đạt chuẩn: Lưu vào Kho Đánh giá
                                         └──> Sai trích dẫn: Tự động sửa hoặc Loại bỏ
                                         │
 7. GIAO DIỆN & BÁO CÁO                  ▼
    [ Streamlit Workbench / HTML Dashboard ] <── [ summary.json / claims_and_assessments.csv ]
```

## Các Giai Đoạn Thực Thi Của Pipeline
1. **Thu thập tài liệu (Document Ingestion):** Đọc 20 báo cáo phát triển bền vững định dạng PDF (tiếng Anh) từ 5 tập đoàn lớn: Nestlé, Danone, Coca-Cola, P&G và Reckitt.
2. **Chia đoạn & Lập chỉ mục (Chunking & Indexing):** Tách văn bản thành 4.930 đoạn tìm kiếm kèm theo số trang PDF gốc chính xác.
3. **Bộ lọc từ khóa (Keyword Filtering):** Lọc từ tổng số 2.565 trang xuống còn 389 trang chứa nội dung về bao bì nhựa/tái chế để tối ưu chi phí và thời gian xử lý của LLM.
4. **Trích xuất Claim bằng LLM:** Ép mô hình trả về JSON Schema chặt chẽ gồm:
   * `claim_text`: Câu trích dẫn nguyên văn từ văn bản gốc.
   * `claim_type`: Phân loại gồm `target` (mục tiêu), `recyclability` (khả năng tái chế), `recycled_content` (hàm lượng tái chế), `collection_recycling` (thu gom/tái chế thực tế).
   * Metadata định lượng: `value` (giá trị số), `unit` (đơn vị), `target_year` (năm mục tiêu), `measurement_year` (năm đo lường).
5. **Cổng kiểm duyệt nguyên văn (Exact Substring Gatekeeper):** Kiểm tra bắt buộc chuỗi `claim_text` phải tồn tại nguyên vẹn trên đúng trang PDF được trích dẫn (`norm(claim_text) in page_text`). Mọi câu do LLM tự bịa hoặc diễn giải sai sẽ bị loại bỏ ngay lập tức.
6. **Truy xuất bằng chứng bằng BM25 (Top-K Retrieval):** Tìm kiếm 5 đoạn văn bản (`K = 5`) có mức độ liên quan cao nhất trên toàn bộ báo cáo để lấy các định nghĩa, số liệu đối chứng hoặc ghi chú chân trang.
7. **Thẩm định & Gán nhãn (Adjudication & Verification):** Đối chiếu tuyên bố với các đoạn bằng chứng tìm được để phân loại thành 5 nhãn:
   * `supported`: Có bằng chứng tài liệu xác thực rõ ràng trong báo cáo.
   * `insufficient_evidence`: Tuyên bố chung chung hoặc thiếu phương pháp đo lường / năm cơ sở (baseline).
   * `scope_mismatch`: Lẫn lộn phạm vi (ví dụ: lấy số liệu của bao bì giấy/thủy tinh đánh đồng cho bao bì nhựa).
   * `potential_inconsistency`: Số liệu mâu thuẫn giữa các phần hoặc giữa mục tiêu và thực tế.
   * `not_yet_assessable`: Các cam kết mục tiêu tương lai (ví dụ mốc 2025/2030) chưa đến thời hạn đánh giá kết quả.
