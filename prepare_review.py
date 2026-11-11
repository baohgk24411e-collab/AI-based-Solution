"""Create an unlabelled review queue and factual corpus summary. Does not invent gold labels."""
from collections import Counter
from src.common import DATA,ROOT,load_json,save_json,csv_text,digest
from src.pipeline import norm
from src.evaluate import evaluate_saved

def main():
    manifest=load_json(DATA/'manifest.json',[])
    candidates=load_json(DATA/'candidates.json',[])
    stats=load_json(DATA/'corpus_stats.json',[])
    queue=[]
    for report in manifest:
        rows=[c for c in candidates if c['report_id']==report['report_id']]
        # Prefer short quantitative passages for a first pass; this is not a random evaluation sample.
        ranked=sorted(rows,key=lambda c:(not any(ch.isdigit() for ch in c['claim_text']),len(c['claim_text'])))
        for c in ranked[:6]:
            queue.append(dict(c,split=report['split'],is_claim='',human_label='',evidence_pages='',
                              reviewer_1='',reviewer_2='',rationale='',adjudicated=False,origin='unlabelled_queue'))
    (DATA/'annotation_queue.csv').write_text(csv_text(queue),encoding='utf-8-sig')
    save_json(DATA/'annotation_queue.json',queue)
    # Every quote must exist in the cited page, every PDF must match the manifest checksum.
    for report in manifest:
        assert report['status']=='downloaded',report['report_id']
        assert digest((ROOT/report['pdf_path']).read_bytes())==report['sha256']
    assert len({r['sha256'] for r in manifest})==len(manifest)
    parsed={r['report_id']:load_json(DATA/'processed'/f"{r['report_id']}.json") for r in manifest}
    for c in candidates:
        page=parsed[c['report_id']]['pages'][c['source_page']-1]
        assert norm(c['claim_text']) in norm(page['text']),c['claim_id']
    summary=dict(reports=len(manifest),companies=len({r['company'] for r in manifest}),
                 pdf_pages=sum(s['pages'] for s in stats),chunks=sum(s['chunks'] for s in stats),
                 packaging_keyword_pages=sum(s['relevant_pages'] for s in stats),
                 low_text_pages=sum(s['low_text_pages'] for s in stats),
                 unverified_candidate_passages=len(candidates),unlabelled_review_queue=len(queue),
                 splits=dict(Counter(r['split'] for r in manifest)),
                 duplicate_pdfs=0,candidate_source_checks_passed=len(candidates),
                 llm_live_run_status='not_run_no_api_key',human_gold_status='not_available')
    save_json(DATA/'audit.json',summary)
    evaluate_saved()
    print(summary)

if __name__=='__main__':main()
