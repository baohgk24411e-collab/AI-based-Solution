# Hướng dẫn gán nhãn

## Đơn vị và phạm vi

Một claim là một phát biểu có thể kiểm tra về khả năng tái chế, hàm lượng vật liệu tái chế, lượng/tỷ lệ thu gom hoặc tái chế, hoặc mục tiêu tương lai có liên quan đến bao bì nhựa. Một câu có nhiều mệnh đề độc lập có thể tách thành nhiều claim, nhưng phải giữ nguyên văn và phần định nghĩa cần thiết.

Không đưa phát thải, nước, tuyển dụng, từ thiện hoặc chất thải sản xuất chung vào tập claim nếu không liên quan rõ tới bao bì nhựa. Tuyên bố về mọi vật liệu bao bì có thể đưa vào nếu bao gồm nhựa, nhưng phải giữ phạm vi hỗn hợp; không diễn giải thành chỉ số riêng cho nhựa.

## Trường cần đọc

Nguyên văn; công ty; trang PDF; loại claim; kỳ đo lường; năm mục tiêu; vật liệu; địa lý; phạm vi sản phẩm; số liệu; đơn vị; mẫu số; đoạn bằng chứng; nhãn; lý do; tên người đọc; trạng thái kiểm tra chéo.

Năm báo cáo không tự động là kỳ đo của mọi con số. Ô không có thông tin để null hoặc ghi chưa xác định, không tự điền global hay plastic.

## Nhãn

| Nhãn | Điều kiện |
|---|---|
| supported | Bằng chứng tài liệu cụ thể hỗ trợ nội dung và phù hợp kỳ, vật liệu, địa lý, phạm vi |
| insufficient_evidence | Chưa đủ bằng chứng trong phạm vi phần tài liệu đã kiểm tra |
| scope_mismatch | Có bằng chứng nhưng áp dụng cho phạm vi khác; nêu rõ khác gì |
| potential_inconsistency | Có thông tin không nhất quán sau khi đã loại trừ khác kỳ, phạm vi, đơn vị, mẫu số và cập nhật số liệu |
| not_yet_assessable | Đánh giá việc đạt một mục tiêu thuộc tương lai so với kỳ báo cáo chưa có cơ sở thời gian |

`not_assessed`, `unreviewed`, `candidate_needs_review` là trạng thái quy trình, không phải nhãn kết quả. Không ép mọi câu phải vào bốn nhãn ban đầu khi mục tiêu chưa tới hạn.

Nếu có nhiều vấn đề, ưu tiên mâu thuẫn đã xác định trên dữ liệu tương thích, sau đó khác phạm vi, rồi thiếu bằng chứng. Ghi các vấn đề còn lại trong lý do/cờ phụ. Đối với mục tiêu chưa đến hạn, không dùng thiếu số liệu hoàn thành làm bằng chứng mâu thuẫn.

## Các bẫy cần tránh

1. Recyclable không đồng nghĩa recycled. Thu gom không đồng nghĩa tái chế hoàn tất.
2. Recycled content là thành phần đầu vào; recycling rate là một chỉ số dòng vật liệu với mẫu số phải xác định.
3. Reusable, recyclable or compostable là chỉ số gộp, không phải tỷ lệ tái chế riêng.
4. PET bottles excluding caps and labels không đại diện cho mọi bao bì nhựa.
5. Số toàn cầu và số một quốc gia không tự động so sánh được.
6. Số liệu lịch sử được điều chỉnh có chú thích không tự động là mâu thuẫn.
7. Câu được lặp lại ở trang khác không phải bằng chứng độc lập.
8. Không tìm ra bằng chứng bằng BM25 không có nghĩa toàn bộ báo cáo không có bằng chứng.

## Quy trình nhóm

- Chia công ty/báo cáo cho người đọc chính. Mỗi claim có ít nhất một người đọc nguồn.
- Trước khi xem nhãn AI, đọc trang claim và các phần liên quan để tránh bị dẫn dắt.
- Một người khác gán nhãn độc lập cho mẫu kiểm tra chéo; ghi bất đồng và lý do thống nhất.
- Ứng dụng lưu từng bản ghi và chỉ dùng nhãn có origin=human, adjudicated=true cho đánh giá nhãn. Đây là thông tin do người dùng xác nhận, ứng dụng không tự chứng minh có hai người đọc.
- Mẫu trong annotation_queue.csv chỉ là điểm bắt đầu. Phải bổ sung claim máy bỏ sót để đo recall trích xuất.
- Tập test giữ riêng. Không chỉnh prompt dựa trên nhãn test rồi báo cáo đó là kết quả độc lập.

## Thước đo

Verification: confusion matrix, accuracy, macro-F1 trên các claim test đã thống nhất và có dự đoán AI. Báo cáo số mẫu và phân bố từng nhãn. Mã hiện tại tính macro-F1 trên các nhãn xuất hiện trong đáp án hoặc dự đoán và ghi rõ tập nhãn này.

Retrieval: page Recall@k và Hit@k theo trang bằng chứng do người đọc xác định. Độ chính xác trích dẫn cần kiểm tra cả vị trí nguồn lẫn việc đoạn trích có thực sự hỗ trợ lập luận.

Extraction: xác định trước quy tắc ghép claim tương đương, gán nhãn đầy đủ vùng được đánh giá và đếm TP/FP/FN. Chưa có bộ tham chiếu đầy đủ thì không công bố recall/F1 trích xuất. Công cụ hiện tại không tự chấm ghép nghĩa giữa hai cách tách claim.
