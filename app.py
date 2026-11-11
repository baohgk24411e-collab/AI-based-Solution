"""GreenClaim local research workbench. Launch with python launch.py."""
import os
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st
from src.common import DATA, ROOT, load_json, save_json, digest, csv_text
from src.pipeline import BM25, parse_pdf, baseline_candidates, norm
from src.llm import make_client, extract, verify, LABELS, TYPES
from src.numeric import check_rate, DIMENSIONS
from src.evaluate import evaluate_saved

st.set_page_config(page_title='GreenClaim | Evidence Workbench',page_icon='🌿',layout='wide')
st.markdown('''<style>
.stApp {background:#f7faf8;} .block-container {padding-top:2rem;max-width:1450px;}
h1,h2,h3 {color:#164b3b;} [data-testid="stMetric"] {background:white;border:1px solid #dbe7df;padding:14px;border-radius:14px;}
[data-testid="stSidebar"] {background:#eaf2ed;} .eyebrow {letter-spacing:3px;font-size:12px;color:#53796a;font-weight:700;}
.hero {background:#133f32;border-radius:20px;padding:25px 30px;margin-bottom:20px;color:#eef8f1;}
.hero h1 {color:white;margin:4px 0 8px;font-size:38px;} .hero p {color:#c6ddcf;margin:0;}
</style>''',unsafe_allow_html=True)
st.markdown('<div class="hero"><div class="eyebrow" style="color:#a9cfb8">GROUP 10 · AI-BASED SOLUTION</div><h1>GreenClaim</h1><p>Từ tuyên bố môi trường đến bằng chứng có thể kiểm tra.</p></div>',unsafe_allow_html=True)

manifest = load_json(DATA/'manifest.json',[])
stats = load_json(DATA/'corpus_stats.json',[])
all_candidates = load_json(DATA/'candidates.json',[])
with st.sidebar:
    st.header('Evidence Workbench')
    st.caption('Phạm vi: bao bì nhựa · báo cáo FMCG')
    source_mode = st.radio('Nguồn tài liệu',['Bộ 20 báo cáo','Tải PDF của bạn'])
    provider = st.selectbox('Dịch vụ LLM', ['lmstudio', 'gemini'])
    key, base_url = None, None
    if provider == 'lmstudio':
        base_url = st.text_input('LM Studio URL', value=os.getenv('LM_STUDIO_BASE_URL','http://127.0.0.1:1234/v1'))
        model = st.text_input('LM Studio model ID', value=os.getenv('LM_STUDIO_MODEL','qwen2.5-7b-instruct'))
        st.caption('Bật server trong LM Studio và nạp model. Không cần API key.')
    else:
        key = st.text_input('Gemini API key',type='password')
        model = st.text_input('Gemini model ID',value=os.getenv('GEMINI_MODEL',''))
        st.link_button('Mở Google AI Studio','https://aistudio.google.com/')
    st.divider()
    st.caption('Supported = được tài liệu hỗ trợ. Không đồng nghĩa xác minh độc lập hoặc kết luận không greenwashing.')

parsed, report = None, None
if source_mode=='Bộ 20 báo cáo':
    available = [r for r in manifest if (DATA/'processed'/f"{r['report_id']}.json").exists()]
    if available:
        selected = st.selectbox('Chọn báo cáo',available,format_func=lambda r:f"{r['company']} · {r['report_year']} · {r['report_type']}")
        report = selected
        @st.cache_data(show_spinner=False)
        def read_parsed(path, mtime):
            return load_json(path)
        p = DATA/'processed'/f"{report['report_id']}.json"
        parsed = read_parsed(str(p),p.stat().st_mtime)
else:
    uploaded = st.file_uploader('PDF đọc được văn bản, tối đa 50 MB',type=['pdf'])
    cols=st.columns(2)
    company=cols[0].text_input('Tên công ty',value='Uploaded company')
    year=cols[1].number_input('Năm báo cáo',min_value=1990,max_value=2100,value=2024)
    if uploaded:
        body=uploaded.getvalue()
        if len(body)>50*1024*1024 or not body.startswith(b'%PDF-'):
            st.error('PDF không hợp lệ hoặc vượt 50 MB.')
        else:
            rid='upload_'+digest(body)[:12]+'_'+digest([company,year])[:6]
            report=dict(report_id=rid,company=company,report_year=year,source_url='',split='unassigned')
            path=DATA/'uploads'/f'{rid}.pdf'
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(body)
            report['pdf_path']=str(path.relative_to(ROOT))
            try:
                if st.session_state.get('upload_id')!=rid:
                    with st.spinner('Đang đọc PDF...'):
                        st.session_state.upload_parsed=parse_pdf(path,report)
                        st.session_state.upload_id=rid
                parsed=st.session_state.upload_parsed
            except Exception as exc:
                st.error(f'Không đọc được PDF: {exc}')

overview, review, llm_tab, numeric, evaluation = st.tabs(['01 · Dữ liệu','02 · Đọc & đối chiếu','03 · LLM','04 · Kiểm tra số','05 · Đánh giá'])

with overview:
    cols=st.columns(2)+st.columns(2)
    cols[0].metric('Báo cáo đã xử lý',len(stats))
    cols[1].metric('Doanh nghiệp',len({s['company'] for s in stats}))
    cols[2].metric('Trang PDF',sum(s['pages'] for s in stats))
    cols[3].metric('Đoạn ứng viên',len(all_candidates))
    st.info('Các đoạn ứng viên được lọc bằng từ khóa. Chúng chưa phải claim đã xác nhận hoặc kết quả phát hiện greenwashing.')
    if stats:
        st.dataframe(stats,hide_index=True,width='stretch')
    st.download_button('Tải danh mục nguồn CSV',csv_text(manifest).encode('utf-8-sig'),'manifest.csv','text/csv')
    st.download_button('Tải các đoạn ứng viên CSV',csv_text(all_candidates).encode('utf-8-sig'),'candidates.csv','text/csv')
    results = DATA/'results'/'BAO_CAO_PHAN_TICH.md'
    if results.exists():
        st.download_button('Tải báo cáo phân tích LLM', results.read_bytes(), results.name, 'text/markdown')
        st.dataframe(load_json(DATA/'results'/'summary.json', []), hide_index=True)
    st.caption('Coca-Cola: 2022–2025. Nestlé, Danone, P&G, Reckitt: 2021–2024. PDF page bắt đầu từ 1; có thể khác số trang in trong tài liệu.')

if parsed:
    base_candidates = [c for c in all_candidates if c['report_id']==report['report_id']] if source_mode=='Bộ 20 báo cáo' else baseline_candidates(parsed)
    manual=load_json(DATA/'manual_claims'/f"{report['report_id']}.json",[])
    ai_claims=load_json(DATA/'llm_claims'/f"{report['report_id']}.json",{}).get('claims',[])
    candidates=list({c['claim_id']:c for c in base_candidates+manual+ai_claims}.values())
    @st.cache_resource(show_spinner=False)
    def make_index(report_id, content_hash, _chunks):
        return BM25(_chunks)
    index=make_index(report['report_id'],digest(parsed['chunks']),parsed['chunks'])
    with review:
        st.subheader('Đọc nguồn trước khi kết luận')
        term=st.text_input('Lọc đoạn ứng viên',placeholder='recycled content, target, plastic...')
        filtered=[c for c in candidates if term.lower() in c['claim_text'].lower()]
        st.caption(f'{len(filtered)} đoạn · loại claim từ baseline chỉ là gợi ý.')
        if filtered:
            claim=st.selectbox('Đoạn cần kiểm tra',filtered,format_func=lambda c:f"PDF p.{c['source_page']} · {c['claim_text'][:135]}")
            st.session_state['selected_claim']=claim
            st.text(claim['claim_text'])
            st.caption(f"Nguồn: {claim['extraction_method']} · trang PDF {claim['source_page']} · {claim['claim_type']}")
            query=st.text_input('Câu tìm bằng chứng',value=claim['claim_text'],key='query_'+claim['claim_id'])
            k=st.slider('Số đoạn tìm về',3,10,5)
            evidence=index.search(query,k,exclude_text=claim['claim_text'])
            left,right=st.columns([1,1])
            with left:
                st.markdown('**Bằng chứng được tìm bằng BM25**')
                for e in evidence:
                    with st.expander(f"PDF p.{e['pdf_page']} · {e['chunk_id']} · điểm {e['score']:.2f}"):
                        if e['repeats_claim']:
                            st.warning('Đoạn này chứa lại tuyên bố. Việc lặp lại không tự tạo bằng chứng xác minh.')
                        st.text(e['text'])
                        if report.get('source_url'):
                            st.link_button('Mở trang trong PDF nguồn',report['source_url'].split('#')[0]+f"#page={e['pdf_page']}",key=e['chunk_id'])
            with right:
                st.markdown('**Toàn văn trang để xem thêm ngữ cảnh**')
                page_num=st.number_input('Trang PDF',min_value=1,max_value=len(parsed['pages']),value=int(claim['source_page']),key='page_'+claim['claim_id'])
                st.text_area('Văn bản trích xuất',parsed['pages'][page_num-1]['text'],height=400,disabled=True)
                st.caption('Bảng nhiều cột có thể bị mất thứ tự. Kiểm tra PDF gốc trước khi sử dụng số liệu.')
                pdf=ROOT/report.get('pdf_path','')
                if pdf.is_file():
                    st.download_button('Tải PDF gốc',pdf.read_bytes(),pdf.name,'application/pdf')
            with st.form('human_review_'+claim['claim_id']):
                st.markdown('**Gán nhãn của người đọc**')
                reviewer=st.text_input('Tên/mã người gán nhãn')
                is_claim=st.checkbox('Đây là claim phù hợp với phạm vi',value=True)
                claim_type=st.selectbox('Loại claim sau khi đọc',TYPES,index=TYPES.index(claim['claim_type']) if claim['claim_type'] in TYPES else 0)
                label=st.selectbox('Nhãn đánh giá',['unreviewed']+LABELS)
                gold_pages=st.text_input('Trang bằng chứng đã kiểm tra, cách nhau bằng dấu phẩy')
                rationale=st.text_area('Lý do và giới hạn')
                adjudicated=st.checkbox('Đã được người thứ hai kiểm tra và thống nhất')
                if st.form_submit_button('Lưu đánh giá thủ công'):
                    try:
                        pages=[int(p.strip()) for p in gold_pages.split(',') if p.strip()]
                        if not reviewer.strip() or any(p<1 or p>len(parsed['pages']) for p in pages):
                            raise ValueError('Cần mã người đọc và số trang hợp lệ.')
                        if adjudicated and is_claim and (label=='unreviewed' or not rationale.strip()):
                            raise ValueError('Cần nhãn và lý do trước khi xác nhận đã thống nhất.')
                        if is_claim and label in ('supported','scope_mismatch','potential_inconsistency') and not pages:
                            raise ValueError('Nhãn này cần ít nhất một trang bằng chứng.')
                        timestamp=datetime.now(timezone.utc).isoformat()
                        record=dict(claim_id=claim['claim_id'],report_id=report['report_id'],claim_text=claim['claim_text'],
                                    source_page=claim['source_page'],is_claim=is_claim,claim_type=claim_type,label=label,
                                    evidence_pages=pages,rationale=rationale,reviewer=reviewer,adjudicated=adjudicated,
                                    origin='human',timestamp=timestamp)
                        save_json(DATA/'reviews'/(datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'_'+digest(record)[:8]+'.json'),record)
                        st.success('Đã lưu một bản đánh giá mới, giữ lại lịch sử.')
                    except ValueError as exc:
                        st.error(str(exc))
        else:
            st.info('Không có đoạn phù hợp. Bạn có thể thêm claim bị bỏ sót bên dưới.')
        with st.expander('Thêm claim bị bỏ sót từ trang gốc'):
            with st.form('add_claim'):
                mp=st.number_input('Trang chứa claim',1,len(parsed['pages']),1)
                mt=st.text_area('Dán nguyên văn claim từ văn bản trang')
                mk=st.selectbox('Loại',TYPES)
                if st.form_submit_button('Thêm claim'):
                    if len(norm(mt))<15 or norm(mt) not in norm(parsed['pages'][mp-1]['text']):
                        st.error('Đoạn trích phải khớp với văn bản ở trang đã chọn.')
                    else:
                        new=dict(claim_id=report['report_id']+'_'+digest([mp,norm(mt)])[:12],report_id=report['report_id'],
                                 company=report['company'],report_year=report['report_year'],source_page=mp,claim_text=norm(mt),
                                 claim_type=mk,extraction_method='manual',assessment='not_assessed')
                        save_json(DATA/'manual_claims'/f"{report['report_id']}.json",list({c['claim_id']:c for c in manual+[new]}.values()))
                        st.success('Đã thêm. Đổi tab/chọn lại báo cáo để cập nhật danh sách.')

    with llm_tab:
        st.subheader('LLM: trích claim và đối chiếu bằng chứng')
        st.info('LM Studio xử lý tại server đã cấu hình. Nếu chọn Gemini, văn bản gửi tới Google và có thể phát sinh phí. Chỉ gọi LLM khi bấm nút.')
        st.caption('Kết quả được lưu cache theo model, prompt và nội dung đầu vào. Đổi prompt/model sẽ tạo lần chạy mới.')
        relevant_pages=[p['pdf_page'] for p in parsed['pages'] if p['packaging_relevant']]
        selected_pages=st.multiselect('Chọn tối đa 3 trang để trích xuất mỗi lần',range(1,len(parsed['pages'])+1),default=relevant_pages[:2])
        if st.button('Trích claim bằng LLM',type='primary'):
            try:
                if not selected_pages or len(selected_pages)>3:
                    raise ValueError('Chọn 1–3 trang để kiểm soát lượng dữ liệu gửi.')
                client=make_client(provider, model, key, base_url)
                pages=[p for p in parsed['pages'] if p['pdf_page'] in selected_pages]
                with st.spinner('LLM đang trích claim...'):
                    result=extract(client,pages,report)
                previous=load_json(DATA/'llm_claims'/f"{report['report_id']}.json",{})
                old=[c for c in previous.get('claims',[]) if c['source_page'] not in selected_pages]
                run = {k:v for k,v in result.items() if k != 'claims'}
                result['claims']=old+result['claims']
                result['processed_pages']=sorted(set(previous.get('processed_pages',[])+selected_pages))
                previous.update(result)
                previous.setdefault('runs', []).append(run)
                # Interactive runs can use a different model/subset than the batch.
                # Invalidate batch coverage rather than silently mix configurations.
                previous.pop('fingerprint', None)
                save_json(DATA/'llm_claims'/f"{report['report_id']}.json",previous)
                st.success(f"Lưu {len(result['claims'])} claim; {len(result['rejected'])} mục bị loại vì không khớp nguồn/schema.")
                st.json(result)
            except Exception as exc:
                st.error(str(exc))
        current=st.session_state.get('selected_claim')
        if current and current['report_id']==report['report_id']:
            st.divider()
            st.write('Claim đang chọn ở tab 02:')
            st.text(current['claim_text'])
            if st.button('Đối chiếu claim này bằng LLM'):
                try:
                    client=make_client(provider, model, key, base_url)
                    ev=index.search(current['claim_text'],5,exclude_text=current['claim_text'])
                    with st.spinner('Đang đối chiếu và kiểm tra trích dẫn...'):
                        result=verify(client,current,ev)
                    result.update(report_id=report['report_id'],retrieved_chunk_ids=[e['chunk_id'] for e in ev])
                    save_json(DATA/'assessments'/(current['claim_id']+'.json'),result)
                    st.success('Đã lưu kết quả AI; vẫn cần người đọc kiểm tra nội dung.')
                except Exception as exc:
                    st.error(str(exc))
            stored=load_json(DATA/'assessments'/(current['claim_id']+'.json'))
            if stored:
                st.json(stored)
                st.download_button('Xuất kết quả JSON',__import__('json').dumps(stored,ensure_ascii=False,indent=2),'assessment.json','application/json')
        if provider == 'gemini' and not (key or os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')):
            st.warning('Chưa cấu hình API key. Chưa có lần chạy LLM thật được thực hiện trong phần này.')

with numeric:
    st.subheader('Tính lại tỷ lệ với mẫu số rõ ràng')
    st.caption('Nhập số đã kiểm tra trên PDF. Công cụ không tự suy ra số liệu từ bảng bị mất cấu trúc.')
    with st.form('numeric_check'):
        cols=st.columns(2)
        n=cols[0].number_input('Tử số: khối lượng',value=0.0,min_value=0.0)
        nu=cols[0].selectbox('Đơn vị tử số',['t','kg'])
        d=cols[1].number_input('Mẫu số: khối lượng',value=0.0,min_value=0.0)
        du=cols[1].selectbox('Đơn vị mẫu số',['t','kg'])
        claimed=st.number_input('Tỷ lệ báo cáo (%)',0.0,100.0,0.0)
        scope={}
        for dim,label in [('company','Công ty'),('year','Kỳ đo lường'),('material','Vật liệu'),('geography','Địa lý'),('boundary','Phạm vi sản phẩm/hoạt động'),('measurement_basis','Cơ sở đo (ví dụ khối lượng bao bì đưa ra thị trường)')]:
            scope[dim]=st.text_input(label,key='num_'+dim)
        description=st.text_input('Tên chỉ số (ví dụ: nhựa tái chế / tổng nhựa sử dụng)')
        pages=st.text_input('Trang nguồn của hai số')
        confirmed=st.checkbox('Tôi đã xác nhận hai số cùng kỳ, vật liệu, địa lý, phạm vi và cơ sở đo')
        if st.form_submit_button('Kiểm tra phép tính'):
            if not confirmed or not description.strip() or not pages.strip():
                st.error('Cần tên chỉ số, trang nguồn và xác nhận tính tương thích.')
            else:
                result=check_rate(dict(scope,value=n,unit=nu),dict(scope,value=d,unit=du),claimed)
                st.json(result)

with evaluation:
    st.subheader('Đánh giá thực nghiệm')
    result=evaluate_saved()
    if result['n']==0:
        st.warning('Chưa có cặp dự đoán AI và nhãn người đọc đã thống nhất trên tập test. Chưa thể báo cáo accuracy hoặc F1.')
    st.json(result)
    st.markdown('**Quy trình:** đọc độc lập → lưu nhãn → người thứ hai kiểm tra → chốt prompt trên development → chạy test → tổng hợp lỗi.')
    st.caption('Bộ chia: 10 báo cáo development / 10 test theo công ty và thời gian. Không được dùng test để chỉnh prompt rồi gọi là kiểm tra độc lập.')
    st.caption('Recall trích xuất chỉ có ý nghĩa sau khi đọc đầy đủ các phần liên quan và bổ sung claim bị bỏ sót. Chấm riêng claim máy tìm được không đo được recall.')
    st.download_button('Tải kết quả đánh giá',__import__('json').dumps(result,ensure_ascii=False,indent=2),'evaluation.json','application/json')

if not parsed:
    st.info('Chưa có tài liệu đã xử lý. Chạy python -m src.pipeline hoặc tải PDF để bắt đầu.')
