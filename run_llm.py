"""Explicit bounded API batch runner. Requires GEMINI_API_KEY and GEMINI_MODEL."""
import argparse
from src.common import DATA,load_json,save_json
from src.llm import Gemini,extract,verify
from src.pipeline import BM25

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',required=True,help='Report ID from manifest.json')
    p.add_argument('--stage',choices=['extract','verify'],default='extract')
    p.add_argument('--max-calls',type=int,default=2,help='Upper limit of API operations this run')
    p.add_argument('--model',default=None)
    args=p.parse_args()
    if args.max_calls<1 or args.max_calls>100:
        p.error('--max-calls must be 1..100')
    manifest={r['report_id']:r for r in load_json(DATA/'manifest.json',[])}
    if args.report not in manifest:
        p.error('Unknown report ID')
    parsed=load_json(DATA/'processed'/f'{args.report}.json')
    if not parsed:p.error('Run src.pipeline first')
    client=Gemini(model=args.model)
    target=DATA/'llm_claims'/f'{args.report}.json'
    saved=load_json(target,dict(claims=[],processed_pages=[],runs=[]))
    if args.stage=='extract':
        pages=[page for page in parsed['pages'] if page['packaging_relevant'] and page['pdf_page'] not in saved['processed_pages']]
        for i in range(min(args.max_calls,len(pages))):
            result=extract(client,[pages[i]],manifest[args.report])
            saved['claims']=list({c['claim_id']:c for c in saved['claims']+result['claims']}.values())
            saved['processed_pages']=sorted(set(saved['processed_pages']+result['processed_pages']))
            saved.setdefault('runs',[]).append(dict(metadata=result['metadata'],processed_pages=result['processed_pages'],rejected=result['rejected']))
            save_json(target,saved)
            print('Processed page',pages[i]['pdf_page'],'accepted',len(result['claims']),'rejected',len(result['rejected']))
        print('Coverage:',len(saved['processed_pages']),'pages. Keyword prefilter may miss claims; human audit required.')
    else:
        index=BM25(parsed['chunks'])
        claims=[c for c in saved['claims'] if not (DATA/'assessments'/(c['claim_id']+'.json')).exists()]
        for c in claims[:args.max_calls]:
            evidence=index.search(c['claim_text'],5,exclude_text=c['claim_text'])
            result=verify(client,c,evidence)
            result.update(report_id=args.report,retrieved_chunk_ids=[e['chunk_id'] for e in evidence])
            save_json(DATA/'assessments'/(c['claim_id']+'.json'),result)
            print(c['claim_id'],result['label'])

if __name__=='__main__':main()
