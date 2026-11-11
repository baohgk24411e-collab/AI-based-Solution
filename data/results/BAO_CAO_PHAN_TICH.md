# Kết quả phân tích 20 báo cáo PTBV

Cập nhật (UTC): 2026-11-11T16:32:01.433317+00:00

Độ phủ hiện tại: 388/389 trang qua bộ lọc; 631 claim được chấp nhận; 560 đối chiếu hợp lệ; 71 claim chưa có đối chiếu hợp lệ.

Model/provider từng báo cáo có trong summary.csv. Metadata từng lần gọi gồm thời gian UTC, token và cache; bản ghi AI chưa được người đọc xác nhận.

Phạm vi: tuyên bố về bao bì nhựa; không phải đánh giá toàn bộ ESG. Toàn bộ văn bản PDF được lập chỉ mục; LLM trích claim trên các trang qua bộ lọc từ khóa. Các trang còn lại chưa được LLM đọc.

Nhãn là nhận định AI cần người đọc kiểm tra. Supported chỉ là hỗ trợ trong tài liệu, không xác minh độc lập. Không có nhãn chuẩn nên chưa tính accuracy/F1. PDF ảnh và bảng mất cấu trúc có thể bị bỏ sót.

| Báo cáo | Trang LLM / trang lọc | Claim | Supported | Thiếu bằng chứng | Khác phạm vi | Có thể mâu thuẫn | Chưa tới hạn | Chưa đánh giá |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| nestle_2021 | 12/12 | 17 | 8 | 9 | 0 | 0 | 0 | 0 |
| nestle_2022 | 16/16 | 17 | 11 | 5 | 0 | 0 | 0 | 1 |
| nestle_2023 | 20/20 | 38 | 20 | 17 | 0 | 0 | 0 | 1 |
| nestle_2024 | 6/6 | 7 | 5 | 2 | 0 | 0 | 0 | 0 |
| danone_2021 | 25/25 | 27 | 15 | 8 | 0 | 0 | 0 | 4 |
| danone_2022 | 30/30 | 34 | 20 | 6 | 0 | 0 | 1 | 7 |
| danone_2023 | 55/56 | 62 | 42 | 6 | 0 | 0 | 0 | 14 |
| danone_2024 | 63/63 | 75 | 51 | 12 | 0 | 0 | 0 | 12 |
| cocacola_2022 | 29/29 | 58 | 36 | 19 | 0 | 0 | 0 | 3 |
| cocacola_2023 | 3/3 | 11 | 7 | 2 | 0 | 0 | 0 | 2 |
| cocacola_2024 | 5/5 | 9 | 7 | 1 | 0 | 0 | 0 | 1 |
| pg_2021 | 2/2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| pg_2022 | 4/4 | 16 | 11 | 5 | 0 | 0 | 0 | 0 |
| pg_2023 | 10/10 | 17 | 10 | 5 | 0 | 0 | 1 | 1 |
| pg_2024 | 4/4 | 5 | 2 | 3 | 0 | 0 | 0 | 0 |
| reckitt_2021 | 28/28 | 68 | 40 | 21 | 0 | 0 | 1 | 6 |
| reckitt_2022 | 30/30 | 58 | 32 | 19 | 0 | 0 | 0 | 7 |
| reckitt_2023 | 24/24 | 43 | 28 | 11 | 0 | 0 | 0 | 4 |
| reckitt_2024 | 17/17 | 51 | 26 | 19 | 0 | 0 | 1 | 5 |
| cocacola_2025 | 5/5 | 17 | 7 | 7 | 0 | 0 | 0 | 3 |

## Chi tiết cần rà soát

Toàn bộ claim, lý do và trích dẫn nằm trong claims_and_assessments.csv / .json. Các đoạn bị loại được giữ trong data/llm_claims; lỗi chạy nằm trong data/batch_errors.json.

### nestle_2021

- PDF trang 3 — **insufficient_evidence**: Plastic packaging designed for recycling
8.1%
  报告中提到的塑料包装设计用于回收的比例为8.1%，但没有提供具体的年份或材料范围。此外，该比例与其他数据混在一起，并未单独列出，难以确认其准确性。
- PDF trang 4 — **supported**: By 2025, 100% of our packaging will be recyclable or reusable and we will reduce our use of virgin plastics by one third.
  Hợp đồng với tuyên bố vì văn bản cung cấp thông tin xác nhận rằng Nestlé sẽ đạt được mục tiêu 100% bao bì tái sử dụng hoặc tái chế vào năm 2025 và giảm sử dụng nhựa nguyên sinh một phần ba vào cùng thời điểm này.
- PDF trang 34 — **insufficient_evidence**: We will make 100% of our packaging recyclable or reusable* by 2025
  Báo cáo không cung cấp dữ liệu cụ thể về tỷ lệ bao bì tái sử dụng hoặc tái chế vào năm 2025 như tuyên bố. Chỉ có mục tiêu là 100% bao bì sẽ tái sử dụng hoặc tái chế được, nhưng không có thông tin về tiến trình đạt được.
- PDF trang 34 — **supported**: We will reduce our use of virgin plastics by one third by 2025
  Báo cáo xác nhận mục tiêu giảm sử dụng nhựa nguyên sinh một phần ba vào năm 2025.
- PDF trang 34 — **insufficient_evidence**: 85.4% Packaging recyclable or reuseable***
  Báo cáo chỉ đề cập đến 85.4% bao bì tái sử dụng hoặc tái chế, nhưng không phân biệt rõ giữa tái sử dụng và tái chế. Không có thông tin về tỷ lệ riêng lẻ của từng loại.

### nestle_2022

- PDF trang 3 — **supported**: By 2025, we aim to design above 95% of our plastic packaging for recycling and continue to work toward 100% being recyclable or reusable Percentage of plastic packaging designed for recycling7 (%) 74.8% 74.9% 81.9%
  Báo cáo của Nestlé xác nhận mục tiêu thiết kế hơn 95% bao bì nhựa cho tái chế vào năm 2025, tương ứng với phần trăm bao bì nhựa được thiết kế để tái chế là 81.9%. Điều này hỗ trợ tuyên bố trong yêu cầu.
- PDF trang 43 — **supported**: We aim to reduce our use of virgin plastics by one third by 2025 (versus 2018 baseline)
  Báo cáo của Nestlé xác nhận mục tiêu giảm sử dụng nhựa nguyên sinh một phần ba so với năm 2018 vào năm 2025. Trích dẫn từ trang 43: 'We aim to reduce our use of virgin plastics by one third by 2025 (versus 2018 baseline)'.
- PDF trang 43 — **supported**: We aim for >95% of our plastic packaging to be designed for recycling by 2025
  文字段落明确支持了该声明，指出Nestlé的目标是在2025年前使超过95%的塑料包装设计为可回收。具体见原文：“By 2025, we aim to design above 95% of our plastic packaging for recycling and continue to work toward 100% being recyclable or reusable Percentage of plastic packaging designed for recycling7 (%)”，以及“我们旨在到2025年使超过95%的塑料包装设计为可回收”。
- PDF trang 43 — **supported**: Percentage of packaging that is reusable, recyclable or compostable* 85.8% (85.4% in 2021)
  Dữ liệu trong báo cáo hỗ trợ tuyên bố về tỷ lệ bao bì tái sử dụng, tái chế hoặc phân hủy sinh học là 85.8% (trong năm 2021 là 85.4%).
- PDF trang 44 — **supported**: We are part of the Ellen MacArthur Foundation’s New Plastics Economy – an initiative that mobilized the first voluntary industry action in 2017 – and we have pledged to work as an industry to create a circular economy for plastic.
  Báo cáo xác nhận rằng Nestlé đã tham gia vào Ellen MacArthur Foundation’s New Plastics Economy từ năm 2017 và cam kết làm việc với ngành để tạo ra một kinh tế tái chế cho nhựa. Điều này tương thích với tuyên bố của công ty.

### nestle_2023

- PDF trang 3 — **supported**: By 2025, we aim to design above 95% of our plastic packaging for recycling and continue to work toward 100% being recyclable or reusable Plastic packaging designed for recycling (%) 74.9% 81.9% 83.5%
  Báo cáo xác nhận rằng Nestlé có mục tiêu thiết kế hơn 95% bao bì nhựa cho tái chế vào năm 2025, tương ứng với tuyên bố của công ty.
- PDF trang 3 — **supported**: By 2030, our ambition is to help 10 million young people around the world have access to economic opportunities Millions of young people around the world with access to economic opportunities since 2017 3.8 5.6 7.7
  Báo cáo chỉ rõ mục tiêu giúp 10 triệu thanh niên trên thế giới có cơ hội kinh tế vào năm 2030 và đã đạt được 7.7 triệu thanh niên từ năm 2017, phù hợp với tuyên bố của công ty.
- PDF trang 10 — **supported**: Virgin plastic reduction by one-third by 2025; 14.9% reduction achieved in 2023.
  Dữ liệu chứng minh rằng Nestlé đã giảm nhựa nguyên sinh sử dụng từ 14.9% vào năm 2023 so với mức cơ sở năm 2018, phù hợp với tuyên bố của công ty.
- PDF trang 14 — **insufficient_evidence**: All packaging accounts for 11.70% (or 9.31 million tonnes of CO2e) of the GHG emissions in our net zero commitment.
  Báo cáo không cung cấp đủ thông tin về lượng khí thải CO2e cụ thể từ bao bì so với tổng lượng khí thải. Chỉ có phần trăm của khí thải bao bì trong cam kết net zero được đề cập, nhưng không có số liệu cụ thể về lượng khí thải CO2e.
- PDF trang 39 — **supported**: 70.6% Volume of cocoa sourced from all countries covered by the CLMRS or other dedicated due diligence systems, with mass balance included
  Báo cáo chỉ rõ rằng Nestlé đã thiết lập một chỉ số hiệu suất mới là 70.6% về lượng cacao được nguồn từ tất cả các quốc gia bao phủ bởi CLMRS hoặc hệ thống doanh nghiệp có trách nhiệm khác, với cân bằng khối lượng được bao gồm. Đây chính xác là con số mà tuyên bố đề cập đến.

### nestle_2024

- PDF trang 5 — **insufficient_evidence**: Launched in May 2024, the Nescafé Gold refill paper pack is fully recyclable and uses 97% less packaging weight compared to our Nescafé Gold Blend 200g jars.
  Báo cáo không cung cấp thông tin cụ thể về tỷ lệ tái chế của bao bì Nescafé Gold refill paper pack hay dữ liệu về việc tái chế thực tế. Chỉ có tuyên bố về tính tái chế và giảm trọng lượng bao bì.
- PDF trang 32 — **supported**: We recognize that the packaging we use to protect our food and beverage products ensures their quality and prevents food waste. It can also have an impact on the environment.
  Báo cáo xác nhận rằng Nestlé nhận thức được tác động của bao bì đối với môi trường và cam kết giảm rác thải, tái chế và tìm kiếm các thay thế cho nhựa. Điều này hỗ trợ tuyên bố của công ty.
- PDF trang 32 — **supported**: We have identified five pillars of activity to make our packaging more sustainable (see illustration below).
  Báo cáo xác nhận rằng Nestlé đã xác định năm trụ cột hoạt động để làm cho bao bì của mình trở nên bền vững (xem minh họa dưới đây), như trong tuyên bố.
- PDF trang 32 — **supported**: Nestlé is reducing our use of virgin plastic for packaging, ensuring that as much packaging as possible is designed for recycling or reuse and promoting responsible waste management practices.
  Báo cáo của Nestlé xác nhận họ đang giảm sử dụng nhựa nguyên sinh trong bao bì và đảm bảo rằng càng nhiều bao bì càng được thiết kế để tái chế hoặc tái sử dụng. Điều này phù hợp với tuyên bố của công ty.
- PDF trang 32 — **supported**: We are pioneering the use of alternatives to plastic, novel technologies and innovative solutions to redesign our packaging.
  Báo cáo đề cập đến việc Nestlé đang tiên phong trong việc sử dụng các thay thế cho nhựa, công nghệ mới và giải pháp sáng tạo để tái thiết kế bao bì. Điều này được thể hiện ở đoạn văn trên trang 32.

### danone_2021

- PDF trang 18 — **supported**: in response to growing concerns over the environmental impact of packaging and in keeping with the goal of protecting the planet, the Waters Reporting Entity set ambitious commitments. These include (i) halving its use of virgin PET and moving to 100% rPET across Europe by 2025, (ii) reducing the carbon footprint of its activity, and (iii) ensuring the collective of its water brands achieve the B CorpTM certification (currently 79% B CorpTM).
  Báo cáo xác nhận rằng Waters Reporting Entity của Danone đã đặt mục tiêu giảm sử dụng PET nguyên sinh và chuyển sang 100% rPET ở châu Âu vào năm 2025, tương tự như tuyên bố trong claim.
- PDF trang 18 — **not_assessed**: In 2021, every country where Danone’s water brands are distributed has product ranges with 100% recycled materials.
  
- PDF trang 25 — **supported**: By 2025, Danone targets to design all its packaging so that it is 100% recyclable, reusable or compostable (vs 84% in 2021) and to increase recycled content to more than 50% for all packaging (vs 34% in 2021), specifically for plastics (around 10% in 2021).
  Báo cáo của Danone xác nhận mục tiêu thiết kế tất cả bao bì để tái sử dụng, tái chế hoặc phân hủy (100%) vào năm 2025 và tăng nội dung tái chế lên hơn 50% cho tất cả các loại bao bì (trừ nhựa), cụ thể là nhựa (khoảng 10% năm 2021).
- PDF trang 46 — **supported**: by replacing polystyrene containers with PET (recyclable material), such as for Activia in the United Kingdom, or by launching Two Good brand products containing fruit from sustainable sources in the United States;
  Báo cáo đề cập đến việc thay thế các chai polystyrene bằng PET (một vật liệu tái chế) cho Activia tại Anh, như trong tuyên bố của Danone.
- PDF trang 46 — **insufficient_evidence**: Danone updated its bottles in Turkey to use up to 15% less plastic;
  Báo cáo không cung cấp thông tin cụ thể về việc Danone đã sử dụng bao bì nhựa giảm tới 15% trong nước Thổ Nhĩ Kỳ. Chỉ có thông tin chung về các nỗ lực cải tiến bao bì.

### danone_2022

- PDF trang 27 — **supported**: Danone aims to (i) have 100% of its packaging to be reusa-ble, recy-
clable or compostable by 2030, (ii) half the use of virgin fossil-based 
packaging by 2040, with 30% reduction by 2030, accelerating reuse 
and recycled materials and (iii) lead the development of effective 
collection systems to recover as much plastic as the Group uses 
by 2040.
  Báo cáo của Danone xác nhận mục tiêu có 100% bao bì tái sử dụng, tái chế hoặc phân hủy được vào năm 2030, đồng thời đề cập đến việc giảm sử dụng nhựa nguyên sinh bằng 50% vào năm 2040 với mức giảm 30% vào năm 2030. Điều này tương ứng với tuyên bố của công ty.
- PDF trang 27 — **supported**: Since 2018, Danone has demonstrated tangible progress in key areas 
such as in virgin plastic reduction, reuse, recycla-bility rate and 
recycled content. In 2022, 84% of its packaging are already reusable, 
recyclable and compostable.
  Báo cáo cung cấp thông tin rằng từ năm 2018, Danone đã đạt được tiến bộ đáng kể trong các lĩnh vực như giảm nhựa nguyên sinh, tái sử dụng, khả năng tái chế và nội dung tái chế. Báo cáo cũng xác nhận rằng vào năm 2022, 84% bao bì của Danone là tái sử dụng, tái chế hoặc phân hủy.
- PDF trang 46 — **supported**: In Uruguay the Salus Brand relaunch it´s iconic jug 6,25 Lt with 7.6% less plastic with same consumer experience.
  Báo cáo cung cấp thông tin về việc relaunch sản phẩm Salus Brand jug 6,25 Lt với 7.6% nhựa ít hơn tại Uruguay, phù hợp với tuyên bố.
- PDF trang 46 — **insufficient_evidence**: Evian launched first sparkling natural mineral water in cans.
  Báo cáo không cung cấp thông tin cụ thể về việc Evian ra mắt chai nước khoáng có gas đầu tiên. Các nội dung trong báo cáo đề cập đến các sáng tạo và cải tiến khác, nhưng không xác nhận sự kiện này.
- PDF trang 151 — **supported**: Danone’s ambition is to transform its value chain by developing solutions that preserve and regenerate nature.
  Đoạn văn bản cung cấp thông tin về chiến lược của Danone nhằm tái tạo và bảo vệ tự nhiên, đồng thời xác nhận mục tiêu này trong báo cáo.

### danone_2023

- PDF trang 28 — **supported**: have 100% of its packaging to be reusable, recyclable, or compostable by 2030;
  Báo cáo cung cấp thông tin rằng Danone có mục tiêu thiết kế bao bì để tái sử dụng, tái chế hoặc phân hủy sinh học vào năm 2030. Điều này được đề cập trong nhiều đoạn văn khác nhau của báo cáo.
- PDF trang 28 — **not_assessed**: halve the use of virgin fossil-based packaging by 2040, with 30% reduction by 2030, accelerating reuse and recycled materials;
  
- PDF trang 28 — **not_assessed**: lead the development of effective collection systems to recover as much plastic as the Group uses by 2040.
  
- PDF trang 50 — **not_assessed**: evian in France and Bonafont in Mexico launched a label-free bottle. The design has been created to achieve a circular packaging solution; it is recyclable and made with 100% recycled plastic excluding cap, whilst being label-free.
  
- PDF trang 182 — **not_assessed**: Danone aims for all packaging to be reusable, recyclable, or compostable by 2030.
  

### danone_2024

- PDF trang 32 — **supported**: have 100% of its packaging to be reusable, recyclable, or compostable by 2030;
  Báo cáo của Danone xác nhận mục tiêu 100% bao bì tái sử dụng, tái chế hoặc phân hủy được vào năm 2030. Các đoạn văn bản từ trang 214 và 356 đều đề cập đến mục tiêu này.
- PDF trang 32 — **not_assessed**: halve the use of virgin fossil-based packaging by 2040, with 30% reduction by 2030, accelerating reuse and recycled materials;
  
- PDF trang 32 — **supported**: lead the development of effective collection systems to recover as much plastic as the Group uses by 2040.
  Báo cáo của Danone xác nhận mục tiêu phát triển hệ thống thu gom hiệu quả để tái chế lượng nhựa sử dụng bằng năm 2040. Các đoạn văn bản trong báo cáo đều đề cập đến cùng một mục tiêu này.
- PDF trang 55 — **insufficient_evidence**: In the United States, Danone expanded the successful and innovative platform of cold foam creamers to Silk and Dunkin brands.
  Báo cáo không cung cấp thông tin cụ thể về việc Danone mở rộng thành công và sáng tạo nền tảng kem lạnh cho các thương hiệu Silk và Dunkin tại Mỹ vào năm 2024.
- PDF trang 55 — **insufficient_evidence**: In the United States, another big project was the harmonization of the yogurt cups for lightweighting and design for recyclability.
  Báo cáo không cung cấp thông tin cụ thể về việc harmonization của các ly chua kem tại Mỹ đã cải thiện khả năng tái chế như thế nào. Chỉ đề cập đến mục tiêu tổng quát về tái chế 100% bao bì vào năm 2030.

### cocacola_2022

- PDF trang 4 — **supported**: In 2022, we collected 61% of the equivalent bottles and cans that we introduced into the market and used 15% rPET in our bottles.
  Báo cáo cung cấp thông tin rằng Coca-Cola đã thu gom được 61% của các chai và lọ tương đương mà họ đưa vào thị trường vào năm 2022, phù hợp với tuyên bố trong báo cáo.
- PDF trang 7 — **supported**: Make 100% of our packaging recyclable globally by 2025
  Báo cáo xác nhận mục tiêu làm cho 100% bao bì nhựa của công ty tái chế được toàn cầu vào năm 2025. Trích dẫn từ trang 7: 'Make 100% of our packaging recyclable globally by 2025'.
- PDF trang 7 — **insufficient_evidence**: Use at least 50% recycled content in our packaging by 2030
  Báo cáo chỉ đề cập đến việc sử dụng 15% rPET trong chai nhựa và 25% tổng lượng vật liệu tái chế được sử dụng vào năm 2022, không có thông tin cụ thể về việc đạt 50% nội dung tái chế vào năm 2030.
- PDF trang 7 — **supported**: Collect and recycle a bottle or can for each one we sell by 2030
  Báo cáo xác nhận mục tiêu tái chế một chai hoặc lon cho mỗi sản phẩm bán ra vào năm 2030 thông qua đoạn văn: 'Collect and recycle a bottle or can for each one we sell by 2030'.
- PDF trang 7 — **insufficient_evidence**: 15% of PET used is recycled PET (rPET)
  Báo cáo không cung cấp dữ liệu cụ thể về tỷ lệ PET tái chế được sử dụng trong năm 2022.

### cocacola_2023

- PDF trang 5 — **supported**: Our global World Without Waste strategy focuses on measurable and interconnected actions under three pillars: DESIGN, COLLECT and PARTNER.
  Công ty đã đề cập đến chiến lược World Without Waste với ba trụ cột chính: DESIGN, COLLECT và PARTNER. Điều này tương đồng với tuyên bố của công ty.
- PDF trang 5 — **supported**: GOAL: Make 100% of our packaging recyclable globally1 by 2025.
  Báo cáo xác nhận rằng Coca-Cola đang hướng tới mục tiêu làm cho 100% bao bì của họ tái chế được toàn cầu vào năm 2025. Trong báo cáo, có ghi rõ: 'GOAL: Make 100% of our packaging recyclable globally1 by 2025.'
- PDF trang 5 — **insufficient_evidence**: GOAL: Use at least 50% recycled content in our packaging by 2030.
  Báo cáo chỉ đề cập đến việc sử dụng 27% chất tái chế trong bao bì chính vào năm 2023, không có thông tin về mục tiêu sử dụng 50% chất tái chế vào năm 2030.
- PDF trang 5 — **supported**: GOAL: Collect and recycle a bottle or can for each one we sell by 2030.
  Báo cáo xác nhận mục tiêu của Coca-Cola là thu gom và tái chế một chai hoặc lon cho mỗi sản phẩm họ bán vào năm 2030. Điều này được đề cập trong phần 'Collect' của chiến lược Without Waste.
- PDF trang 5 — **not_assessed**: GOAL: Have at least 25% of our beverages worldwide by volume sold in refillable/returnable glass or plastic bottles or in fountain dispensers with reusable packaging by 2030.
  

### cocacola_2024

- PDF trang 6 — **insufficient_evidence**: 99% OF OUR PACKAGES WERE RECYCLABLE2 GLOBALLY IN 2024.
  Báo cáo chỉ đề cập đến tỷ lệ bao bì có thể tái chế toàn cầu là 99% vào năm 2024, nhưng không cung cấp bằng chứng về việc thực tế đã tái chế được bao nhiêu bao bì. Không có thông tin cụ thể về lượng bao bì thực tế đã được tái chế.
- PDF trang 6 — **supported**: USED 28% OF RECYCLED MATERIAL 3 IN OUR GLOBAL PRIMARY PACKAGING IN 2024.
  Báo cáo xác nhận rằng Coca-Cola đã sử dụng 28% vật liệu tái chế trong bao bì tiêu dùng chính toàn cầu vào năm 2024.
- PDF trang 6 — **supported**: 18% OF PET USED WAS RECYCLED PET (rPET) 4 IN 2024.
  Báo cáo cung cấp thông tin rằng 18% của PET sử dụng là PET tái chế (rPET) vào năm 2024, phù hợp với tuyên bố.
- PDF trang 10 — **supported**: Percent of the equivalent bottles and cans introduced into the market that were collected and refilled or collected for recycling1 • The Coca-Cola system 61% 62% 65%
  Báo cáo cung cấp dữ liệu chính xác về tỷ lệ bottles và cans được thu gom và tái chế hoặc tái sử dụng, phù hợp với tuyên bố của Coca-Cola.
- PDF trang 10 — **supported**: Percent of recycled material2 used in global primary consumer packaging3 • The Coca-Cola system 25% 27% 28%
  Báo cáo cung cấp thông tin chính xác về tỷ lệ sử dụng vật liệu tái chế trong bao bì tiêu dùng chủ yếu toàn cầu là 28%, phù hợp với tuyên bố.

### pg_2021

- PDF trang 13 — **insufficient_evidence**: In 2021, 73% of our consumer packaging is recyclable or reusable, and we continue to work towards 100% recyclable or reusable consumer packaging.
  Báo cáo chỉ đề cập đến việc 73% bao bì tiêu dùng của P&G trong năm 2021 là tái chế hoặc tái sử dụng được, nhưng không cung cấp chi tiết về các loại bao bì plastic. Không có thông tin xác thực về tỷ lệ tái chế thực tế hay mục tiêu cụ thể.

### pg_2022

- PDF trang 26 — **supported**: At P&G, we are working to design all our consumer packaging to be recyclable or reusable by 2030.
  Báo cáo của P&G xác nhận họ đang làm việc để thiết kế tất cả bao bì tiêu dùng cho sản phẩm của mình là tái sử dụng hoặc tái chế vào năm 2030, tương tự với tuyên bố trong báo cáo.
- PDF trang 27 — **supported**: Our brands, suppliers and partners continue to collaborate on a range of sustainable solutions and on driving circularity so that plastic is collected, recycled and reused.
  Báo cáo cho thấy Procter & Gamble đang hợp tác với các thương hiệu, nhà cung cấp và đối tác để phát triển các giải pháp bền vững và thúc đẩy sự tái sử dụng nhựa. Điều này tương đồng với tuyên bố của công ty.
- PDF trang 27 — **supported**: To track progress toward our goals, P&G considers packaging to be recyclable if there is at-scale collection, sorting, processing, and end markets for the material and format in at least one geography. We do not consider waste to energy and conversion to fuels as suitable end markets.
  Công văn đề cập đến tiêu chí xác định bao bì là tái chế nếu có thu gom quy mô lớn, phân loại, xử lý và thị trường cuối cùng cho vật liệu và dạng thức tại ít nhất một khu vực. Điều này phù hợp với tuyên bố của P&G.
- PDF trang 27 — **insufficient_evidence**: 100% of our consumer packaging will be designed to be recyclable or reusable by 2030
  Báo cáo chỉ đề cập đến tiến trình đạt được mục tiêu và không cung cấp dữ liệu cụ thể về việc thiết kế bao bì tiêu dùng để tái sử dụng hoặc tái chế 100% vào năm 2030.
- PDF trang 27 — **supported**: ~79% of our consumer packaging is designed to be recyclable or reusable
  Báo cáo cung cấp thông tin rằng ~79% bao bì tiêu dùng của Procter & Gamble được thiết kế để tái sử dụng hoặc tái chế, phù hợp với tuyên bố.

### pg_2023

- PDF trang 2 — **supported**: We are increasing our use of recycled plastic resin while also decreasing our total use of plastic in packaging – less plastic overall and a higher proportion from recycled sources.
  Báo cáo đề cập đến việc tăng sử dụng nhựa tái chế trong bao bì đồng thời giảm tổng lượng nhựa sử dụng - ít nhựa hơn và tỷ lệ từ nguồn tái chế cao hơn. Điều này tương ứng với tuyên bố của công ty.
- PDF trang 53 — **insufficient_evidence**: This single component package used in China is 40% lighter and 75% less bulky than corrugated flat boxes. This innovative package is made with a recyclable polyethylene film while the multiple inflatable chambers give structural rigidity and puncture-surviving strength that helps secure the product during shipping.
  Báo cáo không cung cấp dữ liệu cụ thể về tỷ lệ tái chế của màng polyethylene film được sử dụng trong bao bì đa thành phần. Chỉ có thông tin về trọng lượng và kích thước giảm so với hộp corrugated.
- PDF trang 59 — **supported**: 100% of our consumer packaging will be designed to be recyclable or reusable
  Báo cáo đề cập đến mục tiêu rằng 100% bao bì tiêu dùng sẽ được thiết kế để tái sử dụng hoặc tái chế. Mặc dù không cung cấp số liệu cụ thể về năm 2030, báo cáo xác nhận rằng công ty đã đạt được tiến bộ đáng kể trong việc thực hiện mục tiêu này.
- PDF trang 59 — **not_assessed**: 78% of our consumer packaging is designed to be recyclable or reusable
  
- PDF trang 59 — **insufficient_evidence**: 14% of our resins (or about 101,000 metric tons) came from recycled sources in 2023.
  Báo cáo không cung cấp thông tin cụ thể về lượng resin tái chế sử dụng trong năm 2023.

### pg_2024

- PDF trang 7 — **insufficient_evidence**: 100% of our consumer packaging will be designed to be recyclable or reusable.
  Báo cáo chỉ đề cập đến việc thiết kế bao bì tiêu dùng để tái sử dụng hoặc tái chế đạt 100% vào năm 2030, nhưng không cung cấp dữ liệu cụ thể về tiến trình thực hiện mục tiêu này.
- PDF trang 7 — **supported**: 80% of consumer packaging is designed to be recyclable or reusable10
  Báo cáo đề cập đến 80% bao bì tiêu dùng được thiết kế để tái sử dụng hoặc tái chế vào năm 2024.
- PDF trang 7 — **insufficient_evidence**: Virgin Plastic Reduction
Reduce our use of virgin petroleum plastic in our consumer packaging by 50% per unit of production (2017 baseline).
  Báo cáo không cung cấp dữ liệu cụ thể về việc giảm sử dụng nhựa nguyên sinh trong bao bì tiêu dùng so với năm 2017. Chỉ có thông tin về tiến trình đạt được từ FY22 đến FY23.
- PDF trang 7 — **insufficient_evidence**: 21% reduction10
  Báo cáo chỉ đề cập đến việc giảm sử dụng nhựa nguyên sinh nhưng không cung cấp dữ liệu về tỷ lệ tái chế.
- PDF trang 7 — **supported**: Recycled plastic resin 116,000 metric tons
Percent total resin from recycled sources 17% recycled resin
  Báo cáo chỉ rõ rằng trong năm tài chính 2023/24, Procter & Gamble đã sử dụng 116,000 tấn nhựa tái chế và tỷ lệ tổng nhựa từ nguồn tái chế là 17%. Điều này phù hợp với tuyên bố của công ty.

### reckitt_2021

- PDF trang 14 — **supported**: More and more, consumers want packaging that’s sustainable, by which they mean packaging that uses less plastic and is recyclable.
  Báo cáo của Reckitt xác nhận rằng ngày càng có nhiều người tiêu dùng muốn bao bì bền vững, nghĩa là sử dụng ít nhựa hơn và tái chế được. Điều này xuất hiện ở trang 14 của báo cáo.
- PDF trang 14 — **supported**: We are reducing waste in our own operations, and it follows that we also don’t want to create waste when people use our products.
  Báo cáo xác nhận rằng Reckitt đang giảm lượng rác thải trong hoạt động của mình và không muốn tạo ra rác thải khi người tiêu dùng sử dụng sản phẩm. Điều này được thể hiện qua việc công ty đã giành giải thưởng cho chai Gaviscon mới, đồng thời cũng đang tìm cách tái chế và tái sử dụng chất thải.
- PDF trang 14 — **insufficient_evidence**: For example, in 2021, our team won the Glass Packaging of the Year prize at the UK Packaging Awards for the newly developed Gaviscon bottle. The pink shrink sleeve has been replaced with a spray coating that significantly improves sustainability by saving plastic – while also not losing that essential ‘stand-out’ factor on the shelf, which helps maintain brand equity.
  Báo cáo không cung cấp thông tin cụ thể về tỷ lệ tái chế của bottle Gaviscon hay các bằng chứng về khả năng tái sử dụng và tái chế.
- PDF trang 14 — **insufficient_evidence**: Even so, we’ve been able to use more recycled paper and cardboard.
  Báo cáo không cung cấp thông tin cụ thể về lượng giấy và carton tái chế được sử dụng trong năm 2021.
- PDF trang 14 — **not_assessed**: We are also continually looking at ways of reducing the amount of material we use in the first place.
  

### reckitt_2022

- PDF trang 4 — **supported**: 25% recycled content in our plastic packaging by 2025
  Báo cáo đề cập đến mục tiêu sử dụng 25% nội dung tái chế trong bao bì nhựa vào năm 2025, trùng khớp với tuyên bố của công ty.
- PDF trang 4 — **insufficient_evidence**: 50% reduction in amount of virgin plastic packaging by 2030 vs 2020
  Báo cáo chỉ đề cập đến việc giảm 7.3% nhựa nguyên sinh trong bao bì vào năm 2022 so với năm 2021, không cung cấp dữ liệu về năm 2020 để xác minh mục tiêu 50% vào năm 2030.
- PDF trang 5 — **supported**: By 2040, we aim to be net zero across our entire value chain.
  Báo cáo của Reckitt đã xác nhận mục tiêu trở thành doanh nghiệp net zero trong toàn bộ chuỗi giá trị vào năm 2040.
- PDF trang 5 — **not_assessed**: These are the pillars of our Sustainability Ambitions. We have set ourselves stretching targets. They include: generating 50% of our net revenue from more sustainable products, using 100% renewable electricity and cutting greenhouse gas emissions by 65% in our operations against a 2015 baseline, all by 2030.
  
- PDF trang 6 — **supported**: In 2022, we launched our first ever paper-based packaging for Finish, beginning with 1,200 Carrefour stores in France. This combines paper with 75% less plastic to make a fully recyclable, stand-up container.
  Báo cáo cung cấp thông tin chi tiết về việc Reckitt đã ra mắt bao bì giấy cho Finish vào năm 2022 tại 1.200 cửa hàng Carrefour ở Pháp, với lượng nhựa giảm 75% so với bao bì hiện có.

### reckitt_2023

- PDF trang 3 — **insufficient_evidence**: We are now targeting the carbon footprint of our products to have a similar impact.
  Báo cáo không cung cấp thông tin cụ thể về mục tiêu giảm carbon footprint của sản phẩm trong năm 2023 hoặc các biện pháp thực hiện. Chỉ có một tuyên bố chung về việc hướng tới mục tiêu này.
- PDF trang 3 — **supported**: We improved progress towards our goal of achieving 50% net revenue from more sustainable products. In 2023, we reached 29.6%, up from 24.4% in 2022.
  Báo cáo cho thấy chúng đã đạt được 29.6% vào năm 2023, tăng từ 24.4% vào năm 2022.
- PDF trang 5 — **not_assessed**: 50% reduction in amount of virgin plastic packaging by 2030
  
- PDF trang 5 — **supported**: 25% recycled content in our plastic packaging by 2025
  Báo cáo đề cập đến mục tiêu 25% nội dung tái chế trong bao bì nhựa của công ty vào năm 2025. Các đoạn văn bản cung cấp thông tin này đều được trích dẫn từ trang 5, 24 và 29 của báo cáo.
- PDF trang 5 — **supported**: 100% of packaging recyclable or reusable by 2025
  Báo cáo đề cập đến mục tiêu 100% bao bì nhựa tái sử dụng hoặc tái chế vào năm 2025, trùng khớp với tuyên bố của công ty.

### reckitt_2024

- PDF trang 11 — **insufficient_evidence**: Plastics and packaging KPIs based on circular economy principles focusing on three KPIs for weight, % PCR content and recyclability
  Báo cáo chỉ đề cập đến việc thiết kế bao bì để cải thiện khả năng tái chế và sử dụng chất thải tái chế (PCR), nhưng không cung cấp thông tin cụ thể về tỷ lệ tái chế của các loại bao bì nhựa mà công ty sản xuất.
- PDF trang 12 — **supported**: In Europe, we’ve increased PCR content in our pre-treatment trigger bottles to 75% and in our powder jars to 70%
  Báo cáo cho biết PCR content trong các chai bơm tiền xử lý đã tăng lên 75% và trong các chai bột tinh thể là 70% tại châu Âu, phù hợp với tuyên bố của công ty.
- PDF trang 12 — **insufficient_evidence**: We increased PCR content in our toilet bowl cleaners to 75% in Europe, 50% in India, and 30% in South Africa*
  Báo cáo không cung cấp đủ thông tin về việc tăng nội dung PCR trong các sản phẩm vệ sinh bồn cầu tại các khu vực Europe, India và South Africa như tuyên bố. Các đoạn trích chỉ đề cập đến một số sản phẩm khác của công ty.
- PDF trang 18 — **insufficient_evidence**: 100% of plastic packaging recyclable or reusable by 2025
  Báo cáo chỉ đề cập đến mục tiêu 100% bao bì nhựa tái sử dụng hoặc tái chế vào năm 2025 nhưng không cung cấp thông tin cụ thể về tiến trình thực hiện. Không có dữ liệu về tỷ lệ tái chế hay tái sử dụng bao bì nhựa trong các năm trước.
- PDF trang 18 — **insufficient_evidence**: 25% recycled content in our plastic packaging by 2025 On track
  Dựa trên thông tin trong báo cáo, mục tiêu 25% nội dung tái chế trong bao bì nhựa của Reckitt dự kiến sẽ được đạt được vào năm 2025. Tuy nhiên, báo cáo chỉ đề cập rằng mục tiêu này đang tiến triển đúng kế hoạch nhưng không cung cấp số liệu cụ thể về tỷ lệ nội dung tái chế hiện tại hay kết quả thực tế trong năm 2024.

### cocacola_2025

- PDF trang 4 — **supported**: • Aim to use 35% to 40% recycled material2 in primary packaging (PET plastic,3 glass and aluminum), including increasing recycled plastic (rPET) use to 30% to 35% globally by 2035.
  Báo cáo cung cấp thông tin về mục tiêu sử dụng 35% đến 40% vật liệu tái chế trong bao bì chính (PET nhựa, thủy tinh và nhôm) vào năm 2035. Điều này tương ứng với tuyên bố của công ty.
- PDF trang 4 — **supported**: • Aim to collect 70% to 75% of the equivalent number of bottles and cans introduced into the market annually by 2035.
  Báo cáo xác nhận mục tiêu thu gom 70% đến 75% số lượng chai và lọ tương đương được đưa vào thị trường hàng năm vào năm 2035.
- PDF trang 6 — **insufficient_evidence**: 99% OF OUR PACKAGES WERE RECYCLABLE2 GLOBALLY IN 2025.
   CLAIM: '99% OF OUR PACKAGES WERE RECYCLABLE GLOBALLY IN 2025.' EVIDENCE: 2025 году все наши упаковочные материалы были перерабатываемыми на 99%. However, the evidence provided does not specify a global scope or explicitly state that all packages were recyclable in 2025. It only mentions that 99% of our primary consumer packaging was recyclable globally by 2025.
- PDF trang 6 — **insufficient_evidence**: 30% RECYCLED MATERIAL3 IN OUR GLOBAL PRIMARY PACKAGING IN 2025.
  Báo cáo chỉ đề cập đến việc sử dụng 30% vật liệu tái chế trong bao bì chính toàn cầu vào năm 2025, nhưng không cung cấp bằng chứng cụ thể về số lượng hoặc loại vật liệu tái chế được sử dụng.
- PDF trang 6 — **insufficient_evidence**: 20% OF PET USED WAS RECYCLED PET (rPET)4 IN 2025.
  Báo cáo chỉ đề cập đến việc sử dụng 30% vật liệu tái chế trong bao bì toàn cầu vào năm 2025, nhưng không cung cấp thông tin cụ thể về tỷ lệ PET tái chế (rPET) được sử dụng. Không có bằng chứng trực tiếp hỗ trợ cho tuyên bố rằng 20% PET sử dụng là rPET.
