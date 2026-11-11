"""Metrics only for explicit human references, never AI-generated 'gold'."""
from collections import Counter
from .common import DATA,load_json,save_json
from .llm import LABELS

def classification_metrics(pairs):
    if not pairs:
        return {'status':'pending_human_labels','n':0,'macro_f1':None,'accuracy':None}
    labels = sorted(set(a for a,b in pairs) | set(b for a,b in pairs))
    confusion = {a:{b:0 for b in labels} for a in labels}
    for gold,pred in pairs:
        confusion[gold][pred] += 1
    per_label = {}
    for label in labels:
        tp = confusion[label][label]
        fp = sum(confusion[a][label] for a in labels if a!=label)
        fn = sum(confusion[label][b] for b in labels if b!=label)
        precision = tp/(tp+fp) if tp+fp else 0
        recall = tp/(tp+fn) if tp+fn else 0
        per_label[label] = dict(precision=precision,recall=recall,
                               f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0,
                               support=sum(confusion[label].values()))
    return dict(status='evaluated_on_reviewed_pairs',n=len(pairs),
                accuracy=sum(a==b for a,b in pairs)/len(pairs),
                macro_f1=sum(v['f1'] for v in per_label.values())/len(labels),
                macro_f1_label_set=labels, per_label=per_label, confusion_matrix=confusion)

def retrieval_metrics(expected_pages, retrieved_pages):
    expected, retrieved = set(expected_pages),set(retrieved_pages)
    if not expected:
        return {'page_recall_at_k':None,'hit_at_k':None}
    return {'page_recall_at_k':len(expected & retrieved)/len(expected),'hit_at_k':int(bool(expected & retrieved))}

def evaluate_saved():
    manifest = {r['report_id']:r for r in load_json(DATA/'manifest.json',[])}
    assessments = {}
    for path in sorted((DATA/'assessments').glob('*.json')):
        result = load_json(path)
        assessments[result['claim_id']] = result
    reviews = {}
    for path in sorted((DATA/'reviews').glob('*.json')):
        r = load_json(path)
        if r.get('origin')=='human':
            reviews[r['claim_id']] = r
    reviews = {cid:r for cid,r in reviews.items() if r.get('adjudicated') is True and r.get('is_claim') is True}
    pairs = []
    for cid,r in reviews.items():
        if manifest.get(r['report_id'],{}).get('split') != 'test':
            continue
        pred = assessments.get(cid)
        if pred and r.get('label') in LABELS and pred.get('label') in LABELS:
            pairs.append((r['label'],pred['label']))
    result = classification_metrics(pairs)
    result.update(human_adjudicated_claims=len(reviews),ai_assessments=len(assessments),
                  note='Conditional verification accuracy on adjudicated test claims with saved AI predictions. Not end-to-end accuracy. No extraction recall without exhaustive annotation. AI-assisted examples excluded.')
    save_json(DATA/'evaluation.json',result)
    return result

if __name__=='__main__':
    import json
    print(json.dumps(evaluate_saved(),indent=2,ensure_ascii=False))
