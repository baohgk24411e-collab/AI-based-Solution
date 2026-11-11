"""Resumable corpus analysis with local LM Studio or explicit Gemini selection."""
import argparse
import re
from html import escape
from collections import Counter
from datetime import datetime, timezone
from src.common import DATA, load_json, save_json, digest, csv_text
from src.llm import make_client, extract, verify, PROMPT_VERSION, LABELS
from src.pipeline import BM25


def export_results(manifest):
    rows, details = [], []
    for report in manifest:
        rid = report['report_id']
        parsed = load_json(DATA/'processed'/f'{rid}.json', {})
        saved = load_json(DATA/'llm_claims'/f'{rid}.json', {})
        claims = saved.get('claims', [])
        counts = Counter()
        for claim in claims:
            assessment = load_json(DATA/'assessments'/f"{claim['claim_id']}.json", {})
            label = assessment.get('label', 'not_assessed')
            counts[label] += 1
            details.append(dict(claim, label=label, rationale=assessment.get('rationale', ''),
                                evidence_refs=assessment.get('evidence_refs', [])))
        selected = [p['pdf_page'] for p in parsed.get('pages', []) if p['packaging_relevant']]
        completed = set(saved.get('processed_pages', []))
        rows.append(dict(report_id=rid, company=report['company'], year=report['report_year'],
                         provider=saved.get('config', {}).get('provider'), model=saved.get('config', {}).get('model'),
                         total_pages=len(parsed.get('pages', [])), selected_pages=len(selected),
                         processed_pages=len(set(selected) & completed), claims=len(claims),
                         rejected=sum(len(r.get('rejected', [])) for r in saved.get('runs', [])),
                         **{label:counts[label] for label in LABELS+['not_assessed']}))
    out = DATA/'results'
    out.mkdir(exist_ok=True)
    save_json(out/'summary.json', rows)
    save_json(out/'claims_and_assessments.json', details)
    (out/'summary.csv').write_text(csv_text(rows), encoding='utf-8-sig')
    (out/'claims_and_assessments.csv').write_text(csv_text(details), encoding='utf-8-sig')
    lines = ['# Kết quả phân tích 20 báo cáo PTBV', '',
             'Cập nhật (UTC): '+datetime.now(timezone.utc).isoformat(), '',
             f"Độ phủ hiện tại: {sum(r['processed_pages'] for r in rows)}/{sum(r['selected_pages'] for r in rows)} trang qua bộ lọc; {sum(r['claims'] for r in rows)} claim được chấp nhận; {sum(r['claims']-r['not_assessed'] for r in rows)} đối chiếu hợp lệ; {sum(r['not_assessed'] for r in rows)} claim chưa có đối chiếu hợp lệ.", '',
             'Model/provider từng báo cáo có trong summary.csv. Metadata từng lần gọi gồm thời gian UTC, token và cache; bản ghi AI chưa được người đọc xác nhận.', '',
             'Phạm vi: tuyên bố về bao bì nhựa; không phải đánh giá toàn bộ ESG. Toàn bộ văn bản PDF được lập chỉ mục; LLM trích claim trên các trang qua bộ lọc từ khóa. Các trang còn lại chưa được LLM đọc.', '',
             'Nhãn là nhận định AI cần người đọc kiểm tra. Supported chỉ là hỗ trợ trong tài liệu, không xác minh độc lập. Không có nhãn chuẩn nên chưa tính accuracy/F1. PDF ảnh và bảng mất cấu trúc có thể bị bỏ sót.', '',
             '| Báo cáo | Trang LLM / trang lọc | Claim | Supported | Thiếu bằng chứng | Khác phạm vi | Có thể mâu thuẫn | Chưa tới hạn | Chưa đánh giá |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in rows:
        lines.append(f"| {r['report_id']} | {r['processed_pages']}/{r['selected_pages']} | {r['claims']} | "+' | '.join(str(r[k]) for k in LABELS+['not_assessed'])+' |')
    lines += ['', '## Chi tiết cần rà soát', '', 'Toàn bộ claim, lý do và trích dẫn nằm trong claims_and_assessments.csv / .json. Các đoạn bị loại được giữ trong data/llm_claims; lỗi chạy nằm trong data/batch_errors.json.', '']
    for r in rows:
        lines += ['### '+r['report_id'], '']
        subset = [c for c in details if c['report_id']==r['report_id']]
        subset.sort(key=lambda c: (c['label'] not in ('potential_inconsistency','scope_mismatch'), c['source_page']))
        for c in subset[:5]:
            lines += [f"- PDF trang {c['source_page']} — **{c['label']}**: {c['claim_text']}", '  '+c['rationale']]
        lines.append('')
    (out/'BAO_CAO_PHAN_TICH.md').write_text('\n'.join(lines), encoding='utf-8')
    headers = ['report_id','processed_pages','selected_pages','claims']+LABELS+['not_assessed']
    titles = dict(report_id='Báo cáo',processed_pages='Trang đã xử lý',selected_pages='Trang qua bộ lọc',
                  claims='Claim',supported='Được tài liệu hỗ trợ',insufficient_evidence='Thiếu bằng chứng',
                  scope_mismatch='Khác phạm vi',potential_inconsistency='Có thể không nhất quán',
                  not_yet_assessable='Chưa tới hạn',not_assessed='Chưa đánh giá')
    table = '<table><tr>'+''.join('<th>'+escape(titles[k])+'</th>' for k in headers)+'</tr>'
    for row in rows:
        table += '<tr>'+''.join('<td>'+escape(str(row[k]))+'</td>' for k in headers)+'</tr>'
    table += '</table>'
    sections = []
    for report in manifest:
        rid = report['report_id']
        section = '<h2>'+escape(rid)+'</h2><p><a href="../raw_pdfs/'+escape(rid)+'.pdf">Mở PDF gốc</a></p>'
        for claim in (c for c in details if c['report_id']==rid):
            section += '<article><b>PDF '+str(claim['source_page'])+' · '+escape(titles[claim['label']])+'</b>'
            section += '<blockquote>'+escape(claim['claim_text'])+'</blockquote><p>'+escape(claim['rationale'])+'</p>'
            for ref in claim['evidence_refs']:
                section += '<p class="source">'+escape(ref['chunk_id'])+': '+escape(ref['quote'])+'</p>'
            section += '</article>'
        sections.append(section)
    html = '''<!doctype html><html lang="vi"><meta charset="utf-8"><title>GreenClaim — Báo cáo phân tích</title>
<style>body{font:16px/1.6 system-ui;margin:40px;color:#183e32}table{border-collapse:collapse;font-size:12px}th,td{border:1px solid #ccd8cf;padding:6px}article{border:1px solid #ccd8cf;padding:18px;margin:16px 0;break-inside:avoid}blockquote{margin:12px 0;color:#333}.source{font-size:13px;color:#53675c}h2{margin-top:40px}@media print{body{margin:12mm}table{font-size:8px}}</style>
<h1>GreenClaim — Phân tích 20 báo cáo PTBV</h1>
<p>Phạm vi: bao bì nhựa. LLM trích claim ở trang qua bộ lọc từ khóa, đối chiếu với 5 đoạn BM25 trong cùng báo cáo. Nhãn AI cần kiểm tra thủ công; supported không phải xác minh độc lập hay kết luận không greenwashing. Chưa có nhãn chuẩn để đo accuracy/F1.</p>'''
    html += '<p>Cập nhật UTC: '+datetime.now(timezone.utc).isoformat()+'</p>'+table+''.join(sections)+'</html>'
    (out/'BAO_CAO_PHAN_TICH.html').write_text(html, encoding='utf-8')
    return rows


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report', default='all')
    p.add_argument('--stage', choices=['extract','verify','all','export'], default='all')
    p.add_argument('--provider', choices=['lmstudio','gemini'], default='lmstudio')
    p.add_argument('--model')
    p.add_argument('--base-url')
    p.add_argument('--max-calls', type=int, default=None)
    args = p.parse_args()
    if args.max_calls is not None and args.max_calls < 1:
        p.error('--max-calls must be positive')
    manifest = load_json(DATA/'manifest.json', [])
    reports = [r for r in manifest if args.report in ('all',r['report_id'])]
    if not reports:
        p.error('Unknown report ID')
    if args.stage == 'export':
        export_results(manifest)
        return
    client = make_client(args.provider, args.model, base_url=args.base_url)
    config = dict(provider=args.provider, model=client.model, prompt_version=PROMPT_VERSION,
                  endpoint=getattr(client, 'base_url', None))
    errors = load_json(DATA/'batch_errors.json', [])
    calls = 0
    for report in reports:
        rid = report['report_id']
        parsed = load_json(DATA/'processed'/f'{rid}.json')
        if not parsed:
            raise RuntimeError(f'Missing processed report: {rid}')
        target = DATA/'llm_claims'/f'{rid}.json'
        saved = load_json(target, dict(claims=[], processed_pages=[], runs=[]))
        fingerprint = digest([config, parsed])
        if saved.get('fingerprint') != fingerprint:
            if args.stage == 'verify':
                raise RuntimeError(f'{rid}: extraction config/source changed; run --stage all first')
            if target.exists():
                save_json(DATA/'run_archive'/f'{rid}_{digest(saved)[:12]}.json', saved)
            saved = dict(claims=[], processed_pages=[], runs=[], fingerprint=fingerprint, config=config)
        if args.stage in ('extract','all'):
            pages = [page for page in parsed['pages'] if page['packaging_relevant'] and page['pdf_page'] not in saved['processed_pages']]
            for page in pages:
                if args.max_calls is not None and calls >= args.max_calls:
                    break
                calls += 1
                try:
                    result = extract(client, [page], report)
                    saved['claims'] = list({c['claim_id']:c for c in saved['claims']+result['claims']}.values())
                    saved['processed_pages'] = sorted(set(saved['processed_pages']+result['processed_pages']))
                    saved['runs'].append({k:v for k,v in result.items() if k!='claims'})
                    save_json(target, saved)
                    print(rid, 'page', page['pdf_page'], 'claims', len(result['claims']), 'rejected', len(result['rejected']), flush=True)
                except (ValueError, RuntimeError) as exc:
                    errors.append(dict(report_id=rid, stage='extract', page=page['pdf_page'], error=str(exc)))
                    save_json(DATA/'batch_errors.json', errors)
                    print(rid, 'ERROR', str(exc), flush=True)
        if args.stage in ('verify','all'):
            index = BM25(parsed['chunks'])
            for claim in saved['claims']:
                path = DATA/'assessments'/f"{claim['claim_id']}.json"
                ev = index.search(claim['claim_text'], 5, exclude_text=claim['claim_text'])
                signature = digest([config, claim, ev])
                previous = load_json(path, {})
                if previous.get('fingerprint') == signature and not re.search('[\u3400-\u9fff]', previous.get('rationale','')):
                    continue
                if args.max_calls is not None and calls >= args.max_calls:
                    break
                calls += 1
                try:
                    result = verify(client, claim, ev)
                    result.update(report_id=rid, fingerprint=signature, retrieved_chunk_ids=[e['chunk_id'] for e in ev])
                    save_json(path, result)
                    print(rid, claim['claim_id'], result['label'], flush=True)
                except (ValueError, RuntimeError) as exc:
                    errors.append(dict(report_id=rid, stage='verify', claim_id=claim['claim_id'], error=str(exc)))
                    save_json(DATA/'batch_errors.json', errors)
                    print(rid, 'ERROR', str(exc), flush=True)
        export_results(manifest)
    export_results(manifest)
    print('Saved data/results; operations:', calls, flush=True)


if __name__ == '__main__':
    main()
