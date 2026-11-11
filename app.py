"""GreenClaim local research workbench. Launch with python launch.py."""
import os
import re
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st
from src.common import DATA, ROOT, load_json, save_json, digest, csv_text
from src.pipeline import BM25, parse_pdf, baseline_candidates, norm
from src.llm import make_client, extract, verify, LABELS, TYPES
from src.numeric import check_rate, DIMENSIONS
from src.evaluate import evaluate_saved

st.set_page_config(page_title='GreenClaim | Evidence Workbench', page_icon='🌿', layout='wide')

st.markdown('''<style>
.stApp {background: #f8faf9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;}
.block-container {padding-top: 1.8rem; max-width: 1450px;}
h1, h2, h3 {color: #134e3f; font-weight: 700;}
[data-testid="stMetric"] {background: white; border: 1px solid #e2ebe6; padding: 16px; border-radius: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);}
[data-testid="stSidebar"] {background: #edf4f0;}
.hero {background: linear-gradient(135deg, #113f32 0%, #1a5644 100%); border-radius: 18px; padding: 26px 32px; margin-bottom: 22px; color: #f0fdf4; box-shadow: 0 4px 12px rgba(17,63,50,0.12);}
.hero h1 {color: #ffffff; margin: 6px 0 8px; font-size: 34px; letter-spacing: -0.5px;}
.hero p {color: #bbf7d0; font-size: 15px; margin: 0;}
.badge {display: inline-block; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;}
.badge-supported {background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0;}
.badge-insufficient_evidence {background: #fef3c7; color: #b45309; border: 1px solid #fde68a;}
.badge-scope_mismatch {background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff;}
.badge-potential_inconsistency {background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca;}
.badge-not_yet_assessable {background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd;}
.badge-not_assessed {background: #f3f4f6; color: #4b5563; border: 1px solid #e5e7eb;}
.card {background: white; border-radius: 12px; padding: 18px 20px; border: 1px solid #e2ebe6; margin-bottom: 14px; box-shadow: 0 1px 3px rgba(0,0,0,0.02);}
.callout {background: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 14px;}
</style>''', unsafe_allow_html=True)

st.markdown('''<div class="hero">
  <div style="font-size:11px; font-weight:700; letter-spacing:2px; color:#86efac; margin-bottom:4px;">GROUP 10 · AI-BASED SOLUTION</div>
  <h1>GreenClaim Workbench</h1>
  <p>Hệ thống AI đối chiếu & thẩm định tính xác thực của tuyên bố môi trường trong báo cáo phát triển bền vững (FMCG).</p>
</div>''', unsafe_allow_html=True)

manifest = load_json(DATA/'manifest.json', [])
stats = load_json(DATA/'corpus_stats.json', [])
all_candidates = load_json(DATA/'candidates.json', [])

with st.sidebar:
    st.header('Cấu hình nghiên cứu')
    st.caption('Phạm vi: bao bì nhựa & tái chế · Báo cáo DN')
    source_mode = st.radio('Nguồn tài liệu', ['Bộ 20 báo cáo', 'Tải PDF của bạn'])
    provider = st.selectbox('Dịch vụ LLM', ['lmstudio', 'gemini'])
    key, base_url = None, None
    if provider == 'lmstudio':
        base_url = st.text_input('LM Studio URL', value=os.getenv('LM_STUDIO_BASE_URL', 'http://127.0.0.1:1234/v1'))
        model = st.text_input('LM Studio model ID', value=os.getenv('LM_STUDIO_MODEL', 'qwen2.5-7b-instruct'))
        st.caption('Chạy cục bộ, không giới hạn quota và bảo mật dữ liệu tuyệt đối.')
    else:
        key = st.text_input('Gemini API key', type='password')
        model = st.text_input('Gemini model ID', value=os.getenv('GEMINI_MODEL', ''))
        st.link_button('Mở Google AI Studio', 'https://aistudio.google.com/')
    st.divider()
    st.caption('Supported = Được tài liệu nguồn xác nhận. Chưa đồng nghĩa với kiểm chứng độc lập bên ngoài.')

parsed, report = None, None
if source_mode == 'Bộ 20 báo cáo':
    available = [r for r in manifest if (DATA/'processed'/f"{r['report_id']}.json").exists()]
    if available:
        selected = st.selectbox('Chọn báo cáo', available, format_func=lambda r: f"{r['company']} · {r['report_year']} · {r['report_type']}")
        report = selected
        @st.cache_data(show_spinner=False)
        def read_parsed(path, mtime):
            return load_json(path)
        p = DATA/'processed'/f"{report['report_id']}.json"
        parsed = read_parsed(str(p), p.stat().st_mtime)
else:
    uploaded = st.file_uploader('PDF đọc được văn bản, tối đa 50 MB', type=['pdf'])
    cols = st.columns(2)
    company = cols[0].text_input('Tên công ty', value='Uploaded company')
    year = cols[1].number_input('Năm báo cáo', min_value=1990, max_value=2100, value=2024)
    if uploaded:
        body = uploaded.getvalue()
        if len(body) > 50*1024*1024 or not body.startswith(b'%PDF-'):
            st.error('PDF không hợp lệ hoặc vượt 50 MB.')
        else:
            rid = 'upload_' + digest(body)[:12] + '_' + digest([company, year])[:6]
            report = dict(report_id=rid, company=company, report_year=year, source_url='', split='unassigned')
            path = DATA/'uploads'/f'{rid}.pdf'
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
            report['pdf_path'] = str(path.relative_to(ROOT))
            try:
                if st.session_state.get('upload_id') != rid:
                    with st.spinner('Đang đọc PDF...'):
                        st.session_state.upload_parsed = parse_pdf(path, report)
                        st.session_state.upload_id = rid
                parsed = st.session_state.upload_parsed
            except Exception as exc:
                st.error(f'Không đọc được PDF: {exc}')

overview, review, llm_tab, numeric, evaluation = st.tabs([
    '01 · Dữ liệu & Tổng quan',
    '02 · Đọc & đối chiếu',
    '03 · LLM Trích xuất',
    '04 · Kiểm tra số & Hallucination',
    '05 · Đánh giá thực nghiệm'
])

with overview:
    # Top 4 metrics required by unit tests and baseline
    cols = st.columns(4)
    cols[0].metric('Báo cáo đã xử lý', len(stats))
    cols[1].metric('Doanh nghiệp', len({s['company'] for s in stats}))
    cols[2].metric('Trang PDF', sum(s['pages'] for s in stats))
    cols[3].metric('Đoạn ứng viên', len(all_candidates))
    
    # Summary of LLM Progress
    summary_path = DATA/'results'/'summary.json'
    summary_data = load_json(summary_path, [])
    if summary_data:
        total_p = sum(r['processed_pages'] for r in summary_data)
        total_sel = sum(r['selected_pages'] for r in summary_data)
        total_claims = sum(r['claims'] for r in summary_data)
        total_supp = sum(r['supported'] for r in summary_data)
        total_insuff = sum(r['insufficient_evidence'] for r in summary_data)
        
        st.markdown('### Kết quả phân tích toàn bộ 20 báo cáo')
        scols = st.columns(4)
        scols[0].metric('Độ phủ trang chọn', f"{total_p}/{total_sel}", delta=f"{total_p/total_sel*100:.1f}%" if total_sel else "0%")
        scols[1].metric('Claims trích xuất', total_claims)
        scols[2].metric('Supported (Có căn cứ)', total_supp)
        scols[3].metric('Thiếu bằng chứng', total_insuff)
        
        st.dataframe(summary_data, hide_index=True, width='stretch')
    elif stats:
        st.dataframe(stats, hide_index=True, width='stretch')

    dcols = st.columns(3)
    dcols[0].download_button('Tải danh mục nguồn CSV', csv_text(manifest).encode('utf-8-sig'), 'manifest.csv', 'text/csv', width='stretch')
    dcols[1].download_button('Tải đoạn ứng viên CSV', csv_text(all_candidates).encode('utf-8-sig'), 'candidates.csv', 'text/csv', width='stretch')
    
    results = DATA/'results'/'BAO_CAO_PHAN_TICH.md'
    if results.exists():
        dcols[2].download_button('Tải báo cáo phân tích MD', results.read_bytes(), results.name, 'text/markdown', width='stretch')

if parsed:
    base_candidates = [c for c in all_candidates if c['report_id'] == report['report_id']] if source_mode == 'Bộ 20 báo cáo' else baseline_candidates(parsed)
    manual = load_json(DATA/'manual_claims'/f"{report['report_id']}.json", [])
    ai_claims = load_json(DATA/'llm_claims'/f"{report['report_id']}.json", {}).get('claims', [])
    candidates = list({c['claim_id']: c for c in base_candidates + manual + ai_claims}.values())
    
    @st.cache_resource(show_spinner=False)
    def make_index(report_id, content_hash, _chunks):
        return BM25(_chunks)
    
    index = make_index(report['report_id'], digest(parsed['chunks']), parsed['chunks'])

    with review:
        st.subheader('Đọc nguồn và kiểm chứng bằng chứng')
        term = st.text_input('Lọc đoạn ứng viên', placeholder='recycled content, target, plastic...')
        filtered = [c for c in candidates if term.lower() in c['claim_text'].lower()]
        st.caption(f'Tìm thấy {len(filtered)} đoạn tuyên bố/ứng viên.')
        
        if filtered:
            claim = st.selectbox('Đoạn cần kiểm tra', filtered, format_func=lambda c: f"PDF p.{c['source_page']} · {c['claim_text'][:120]}")
            st.session_state['selected_claim'] = claim
            
            # Load existing AI assessment if available
            assessment_file = DATA/'assessments'/f"{claim['claim_id']}.json"
            assessment = load_json(assessment_file, {}) if assessment_file.exists() else None
            
            badge_class = f"badge-{assessment['label']}" if assessment and assessment.get('label') in LABELS else "badge-not_assessed"
            badge_text = assessment['label'].replace('_', ' ').upper() if assessment and assessment.get('label') else "CHƯA ĐÁNH GIÁ"
            
            st.markdown(f'''<div class="card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span class="badge {badge_class}">{badge_text}</span>
                    <span style="font-size:12px; color:#6b7280;">Nguồn: <b>{claim.get('extraction_method','baseline')}</b> | Trang PDF: <b>{claim['source_page']}</b> | Loại: <b>{claim.get('claim_type','general')}</b></span>
                </div>
                <div style="font-size:16px; font-weight:500; color:#1f2937; line-height:1.5;">"{claim['claim_text']}"</div>
            </div>''', unsafe_allow_html=True)

            if assessment:
                with st.expander('Xem chi tiết kết quả thẩm định AI', expanded=True):
                    st.markdown(f"**Kết luận AI:** `{assessment.get('label')}`")
                    st.markdown(f"**Lý giải (Tiếng Việt):** {assessment.get('rationale')}")
                    if assessment.get('flags'):
                        st.warning('Cảnh báo rủi ro: ' + '; '.join(assessment['flags']))
                    if assessment.get('evidence_refs'):
                        st.markdown("**Các trích dẫn đối chiếu từ báo cáo:**")
                        for ref in assessment['evidence_refs']:
                            st.info(f"Trang {ref.get('pdf_page')}: \"{ref.get('quote')}\" (Chunk ID: `{ref.get('chunk_id')}`)")

            query = st.text_input('Câu tìm bằng chứng', value=claim['claim_text'], key='query_' + claim['claim_id'])
            k = st.slider('Số đoạn tìm về', 3, 10, 5)
            evidence = index.search(query, k, exclude_text=claim['claim_text'])
            
            left, right = st.columns([1, 1])
            with left:
                st.markdown('**Bằng chứng tìm thấy trong báo cáo (BM25)**')
                for e in evidence:
                    with st.expander(f"PDF p.{e['pdf_page']} · {e['chunk_id']} · Điểm {e['score']:.2f}"):
                        if e['repeats_claim']:
                            st.warning('Đoạn này lặp lại tuyên bố. Không tự tạo bằng chứng xác minh độc lập.')
                        st.text(e['text'])
                        if report.get('source_url'):
                            st.link_button('Mở trang trong PDF gốc', report['source_url'].split('#')[0] + f"#page={e['pdf_page']}", key=e['chunk_id'])
            
            with right:
                st.markdown('**Toàn văn trang PDF tương ứng**')
                page_num = st.number_input('Trang PDF', min_value=1, max_value=len(parsed['pages']), value=int(claim['source_page']), key='page_' + claim['claim_id'])
                st.text_area('Văn bản trích xuất', parsed['pages'][page_num - 1]['text'], height=380, disabled=True)
                pdf = ROOT/report.get('pdf_path', '')
                if pdf.is_file():
                    st.download_button('Tải tệp PDF gốc', pdf.read_bytes(), pdf.name, 'application/pdf')

            with st.form('human_review_' + claim['claim_id']):
                st.markdown('**Gán nhãn chuyên gia (Human Adjudication)**')
                reviewer = st.text_input('Tên/mã người gán nhãn')
                is_claim = st.checkbox('Đây là claim phù hợp với phạm vi bao bì nhựa', value=True)
                claim_type = st.selectbox('Loại claim sau khi đọc', TYPES, index=TYPES.index(claim['claim_type']) if claim['claim_type'] in TYPES else 0)
                label = st.selectbox('Nhãn đánh giá', ['unreviewed'] + LABELS)
                gold_pages = st.text_input('Trang bằng chứng đã kiểm tra (cách nhau bởi dấu phẩy)')
                rationale = st.text_area('Lý do gán nhãn và ghi chú')
                adjudicated = st.checkbox('Đã được người thứ hai thẩm định độc lập')
                if st.form_submit_button('Lưu đánh giá thủ công'):
                    try:
                        pages = [int(p.strip()) for p in gold_pages.split(',') if p.strip()]
                        if not reviewer.strip() or any(p < 1 or p > len(parsed['pages']) for p in pages):
                            raise ValueError('Cần mã người đọc và số trang hợp lệ.')
                        if adjudicated and is_claim and (label == 'unreviewed' or not rationale.strip()):
                            raise ValueError('Cần chọn nhãn và ghi rõ lý do trước khi xác nhận thống nhất.')
                        if is_claim and label in ('supported', 'scope_mismatch', 'potential_inconsistency') and not pages:
                            raise ValueError('Nhãn này bắt buộc phải có ít nhất một trang bằng chứng.')
                        timestamp = datetime.now(timezone.utc).isoformat()
                        record = dict(claim_id=claim['claim_id'], report_id=report['report_id'], claim_text=claim['claim_text'],
                                     source_page=claim['source_page'], is_claim=is_claim, claim_type=claim_type, label=label,
                                     evidence_pages=pages, rationale=rationale, reviewer=reviewer, adjudicated=adjudicated,
                                     origin='human', timestamp=timestamp)
                        save_json(DATA/'reviews'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '_' + digest(record)[:8] + '.json'), record)
                        st.success('Đã lưu bản đánh giá thủ công thành công!')
                    except ValueError as exc:
                        st.error(str(exc))
        else:
            st.info('Không tìm thấy đoạn ứng viên phù hợp với từ khóa.')

    with llm_tab:
        st.subheader('Trích xuất & Đối chiếu tự động với LLM')
        st.info(f"Đang sử dụng dịch vụ: **{provider.upper()}** (Model: `{model}`).")
        relevant_pages = [p['pdf_page'] for p in parsed['pages'] if p['packaging_relevant']]
        selected_pages = st.multiselect('Chọn trang PDF để trích xuất claim (tối đa 3 trang/lượt)', range(1, len(parsed['pages']) + 1), default=relevant_pages[:2])
        if st.button('Trích claim bằng LLM', type='primary'):
            try:
                if not selected_pages or len(selected_pages) > 3:
                    raise ValueError('Vui lòng chọn 1–3 trang để kiểm soát token.')
                client = make_client(provider, model, key, base_url)
                pages = [p for p in parsed['pages'] if p['pdf_page'] in selected_pages]
                with st.spinner('LLM đang trích xuất các tuyên bố...'):
                    result = extract(client, pages, report)
                previous = load_json(DATA/'llm_claims'/f"{report['report_id']}.json", {})
                old = [c for c in previous.get('claims', []) if c['source_page'] not in selected_pages]
                run = {k: v for k, v in result.items() if k != 'claims'}
                result['claims'] = old + result['claims']
                result['processed_pages'] = sorted(set(previous.get('processed_pages', []) + selected_pages))
                previous.update(result)
                previous.setdefault('runs', []).append(run)
                previous.pop('fingerprint', None)
                save_json(DATA/'llm_claims'/f"{report['report_id']}.json", previous)
                st.success(f"Trích xuất thành công {len(result['claims'])} claims; {len(result['rejected'])} mục bị loại bỏ.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))

        current = st.session_state.get('selected_claim')
        if current and current['report_id'] == report['report_id']:
            st.divider()
            st.markdown(f"**Claim đang chọn từ tab 02:** \"{current['claim_text']}\"")
            if st.button('Đối chiếu claim này bằng LLM'):
                try:
                    client = make_client(provider, model, key, base_url)
                    ev = index.search(current['claim_text'], 5, exclude_text=current['claim_text'])
                    with st.spinner('LLM đang đối chiếu bằng chứng...'):
                        result = verify(client, current, ev)
                    result.update(report_id=report['report_id'], retrieved_chunk_ids=[e['chunk_id'] for e in ev])
                    save_json(DATA/'assessments'/(current['claim_id'] + '.json'), result)
                    st.success('Đã lưu kết quả đối chiếu AI.')
                    st.json(result)
                except Exception as exc:
                    st.error(str(exc))

    with numeric:
        st.subheader('Kiểm tra số liệu & Phân tích Hallucination')
        
        # Section 1: Hallucination Audit of Extracted Metrics
        st.markdown('#### 1. Đánh giá tính xác thực của số liệu trích xuất (Hallucination Audit)')
        st.caption('Kiểm tra xem số liệu (value) mà LLM bóc tách có thực sự xuất hiện nguyên văn trong câu claim gốc hay bị ảo giác/nhầm lẫn số liệu lân cận.')
        
        # Load claims and check values
        import glob
        claims_files = glob.glob(str(DATA/'llm_claims'/'*.json'))
        val_match, val_mismatch = [], []
        for cf in claims_files:
            cdata = load_json(cf, {})
            c_rid = Path(cf).stem
            for cl in cdata.get('claims', []):
                val = cl.get('value')
                txt = cl.get('claim_text', '')
                if val is not None:
                    nums_in_txt = re.findall(r'\d+(?:\.\d+)?', txt)
                    floats_in_txt = [float(n) for n in nums_in_txt]
                    try:
                        v_float = float(val)
                        if any(abs(v_float - f) < 1e-4 for f in floats_in_txt):
                            val_match.append(dict(report_id=c_rid, claim_id=cl['claim_id'], value=val, unit=cl.get('unit'), text=txt[:110], status='Grounded 100%'))
                        else:
                            val_mismatch.append(dict(report_id=c_rid, claim_id=cl['claim_id'], value=val, numbers_in_quote=str(floats_in_txt), text=txt[:110], status='Hallucinated/Mismatched'))
                    except Exception:
                        val_mismatch.append(dict(report_id=c_rid, claim_id=cl['claim_id'], value=val, text=txt[:110], status='Hallucinated/Mismatched'))

        n_total = len(val_match) + len(val_mismatch)
        h_cols = st.columns(3)
        h_cols[0].metric('Tổng claims có số liệu', n_total)
        h_cols[1].metric('Chính xác (Grounded 100%)', f"{len(val_match)} ({len(val_match)/n_total*100:.1f}%)" if n_total else "0%")
        h_cols[2].metric('Ảo giác / Sai lệch số', f"{len(val_mismatch)} ({len(val_mismatch)/n_total*100:.1f}%)" if n_total else "0%")

        ha_tab1, ha_tab2 = st.tabs(['Các metric chính xác 100%', 'Các metric bị ảo giác / lệch số'])
        with ha_tab1:
            st.dataframe(val_match, width='stretch')
        with ha_tab2:
            st.warning('Các trường hợp LLM nhặt nhầm số liệu từ bảng/câu kế cận hoặc tự chuyển từ ngữ thành số:')
            st.dataframe(val_mismatch, width='stretch')

        st.divider()
        # Section 2: Mathematical Rate Re-check
        st.markdown('#### 2. Tính lại tỷ lệ với mẫu số tường minh')
        with st.form('numeric_check'):
            cols = st.columns(2)
            n = cols[0].number_input('Tử số: khối lượng', value=0.0, min_value=0.0)
            nu = cols[0].selectbox('Đơn vị tử số', ['t', 'kg'])
            d = cols[1].number_input('Mẫu số: khối lượng', value=0.0, min_value=0.0)
            du = cols[1].selectbox('Đơn vị mẫu số', ['t', 'kg'])
            claimed = st.number_input('Tỷ lệ báo cáo (%)', 0.0, 100.0, 0.0)
            scope = {}
            for dim, label in [('company', 'Công ty'), ('year', 'Kỳ đo lường'), ('material', 'Vật liệu'), ('geography', 'Địa lý'), ('boundary', 'Phạm vi sản phẩm/hoạt động'), ('measurement_basis', 'Cơ sở đo')]:
                scope[dim] = st.text_input(label, key='num_' + dim)
            description = st.text_input('Tên chỉ số (ví dụ: nhựa tái chế / tổng nhựa sử dụng)')
            pages = st.text_input('Trang nguồn của hai số')
            confirmed = st.checkbox('Tôi đã xác nhận hai số cùng kỳ, vật liệu, địa lý, phạm vi và cơ sở đo')
            if st.form_submit_button('Kiểm tra phép tính'):
                if not confirmed or not description.strip() or not pages.strip():
                    st.error('Cần tên chỉ số, trang nguồn và xác nhận tính tương thích.')
                else:
                    result = check_rate(dict(scope, value=n, unit=nu), dict(scope, value=d, unit=du), claimed)
                    st.json(result)

    with evaluation:
        st.subheader('Đánh giá thực nghiệm mô hình')
        eval_result = evaluate_saved()
        if eval_result['n'] == 0:
            st.info('Đang chờ hoàn tất gán nhãn đối ứng trên tập test để tính toán độ chính xác (Accuracy, F1).')
        st.json(eval_result)
        
        rep_file = DATA/'results'/'BAO_CAO_PHAN_TICH.md'
        if rep_file.exists():
            st.markdown('### Xem trước báo cáo phân tích')
            st.markdown(rep_file.read_text(encoding='utf-8'))
            st.download_button('Tải báo cáo phân tích (Markdown)', rep_file.read_bytes(), 'BAO_CAO_PHAN_TICH.md', 'text/markdown')

if not parsed:
    st.info('Vui lòng chọn báo cáo từ danh mục hoặc tải PDF lên để bắt đầu.')
