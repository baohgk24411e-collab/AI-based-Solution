"""Audit accepted local-run outputs against original page text and retrieved chunks."""
from collections import Counter
from src.common import DATA,load_json,save_json
from src.llm import validate_claims,validate_assessment


def main():
    report_rows=[]
    for report in load_json(DATA/'manifest.json',[]):
        rid=report['report_id']
        parsed=load_json(DATA/'processed'/f'{rid}.json')
        saved=load_json(DATA/'llm_claims'/f'{rid}.json',{})
        claims=saved.get('claims',[])
        accepted,rejected=validate_claims({'claims':claims},parsed['pages'],report)
        assert not rejected,(rid,rejected)
        chunks={c['chunk_id']:c for c in parsed['chunks']}
        checked=0
        for claim in claims:
            assessment=load_json(DATA/'assessments'/f"{claim['claim_id']}.json")
            if not assessment:
                continue
            evidence=[chunks[cid] for cid in assessment['retrieved_chunk_ids']]
            validate_assessment(assessment,evidence)
            checked+=1
        row=dict(report_id=rid,pages_processed=len(saved.get('processed_pages',[])),
                 selected_pages=sum(p['packaging_relevant'] for p in parsed['pages']),
                 claims_source_checked=len(accepted),assessments_citations_checked=checked,
                 not_assessed=len(claims)-checked)
        report_rows.append(row)
    result=dict(reports=report_rows,
                note='Exact-source integrity only, not semantic correctness or independent verification.')
    save_json(DATA/'results'/'integrity_audit.json',result)
    print(result)


if __name__=='__main__':
    main()
