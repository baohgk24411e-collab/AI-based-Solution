"""Page-grounded PDF parsing, lexical baseline and BM25 retrieval (CPU only)."""
import argparse
from collections import Counter
import math
import re
import unicodedata

from pypdf import PdfReader
from .common import DATA, ROOT, load_json, save_json, digest, csv_text

VERSION = 'page-chunks-v2-fonttools'
PACKAGING = re.compile(r'\b(plastic|plastics|packaging|bottles?|rpet|pet|hdpe|polyethylene|polypropylene)\b', re.I)
RECYCLING = re.compile(r'\b(recycl\w*|collect\w*|circular\w*|reus\w*|compost\w*)\b', re.I)
TARGET = re.compile(r'\b(aim|aims|target|targets|goal|goals|commit|commitment|committed|will|by 20\d\d)\b', re.I)
STOP = set('the a an and or of to in on for with from by our we is are was were be as at that this it have has had its their all more than which through into'.split())

def norm(text):
    return ' '.join(unicodedata.normalize('NFKC', text).replace('\x00','').split())

def tokens(text):
    return [w for w in re.findall(r'[\w%]+', norm(text).lower()) if w not in STOP]

def relevant(text):
    return bool(PACKAGING.search(text) and RECYCLING.search(text))

def parse_pdf(path, report):
    reader = PdfReader(path)
    if reader.is_encrypted and not reader.decrypt(''):
        raise ValueError('PDF requires a password')
    pages, chunks = [], []
    labels = reader.page_labels
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        base = dict(report_id=report['report_id'], company=report['company'],
                    report_year=report['report_year'], pdf_page=i+1,
                    printed_page=labels[i], source_url=report.get('source_url',''))
        pages.append(dict(base, text=text, character_count=len(norm(text)),
                          needs_ocr=len(norm(text)) < 60, packaging_relevant=relevant(text)))
        # Keep the entire page separately so tables and footnotes remain inspectable.
        clean = norm(text)
        for start in range(0, len(clean), 2100):
            chunk = clean[start:start+2500]
            if not chunk:
                continue
            chunks.append(dict(base, chunk_id=f"{report['report_id']}:p{i+1}:c{start//2100+1}",
                               text=chunk, char_start=start, char_end=start+len(chunk)))
            if start+2500 >= len(clean):
                break
    return dict(version=VERSION, report=report, pages=pages, chunks=chunks)

def baseline_candidates(parsed):
    """Candidate passages, NOT verified claims or greenwashing labels."""
    result, seen = [], set()
    for page in parsed['pages']:
        if not page['packaging_relevant']:
            continue
        clean = norm(page['text'])
        # Sentence-like passages; preserve exact normalized source substring.
        for part in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9])', clean):
            sentence = part.strip()
            if not relevant(sentence) or len(sentence) < 35:
                continue
            if len(sentence) > 900:
                # Tables can form huge non-sentences: present a source window, clearly a candidate.
                hit = RECYCLING.search(sentence)
                start = max(0, hit.start()-200)
                sentence = sentence[start:start+800]
            key = (page['report_id'], sentence.lower())
            if key in seen:
                continue
            seen.add(key)
            kind = ('target' if TARGET.search(sentence) else
                    'recycled_content' if re.search(r'recycled (content|plastic|pet)|rpet', sentence, re.I) else
                    'recyclability' if re.search(r'recyclable|designed for recycl', sentence, re.I) else
                    'collection_recycling')
            result.append(dict(claim_id=page['report_id']+'_'+digest([page['pdf_page'],sentence])[:12],
                               report_id=page['report_id'], company=page['company'], report_year=page['report_year'],
                               source_page=page['pdf_page'], claim_text=sentence, claim_type=kind,
                               scope=None, target_year=None, material=None, value=None, unit=None,
                               extraction_method='keyword_baseline', assessment='not_assessed',
                               review_status='candidate_needs_review'))
    return result

class BM25:
    def __init__(self, chunks):
        self.chunks = chunks
        self.counts = [Counter(tokens(c['text'])) for c in chunks]
        self.lengths = [sum(c.values()) for c in self.counts]
        self.avg = sum(self.lengths)/max(len(chunks), 1) or 1
        self.df = Counter(t for counts in self.counts for t in counts)

    def search(self, query, k=5, exclude_text=None):
        query_tokens = set(tokens(query))
        n = len(self.chunks)
        scored = []
        for chunk, counts, length in zip(self.chunks, self.counts, self.lengths):
            score = 0.0
            for term in query_tokens:
                freq = counts[term]
                if freq:
                    idf = math.log(1+(n-self.df[term]+0.5)/(self.df[term]+0.5))
                    score += idf * freq * 2.5 / (freq + 1.5*(0.25+0.75*length/self.avg))
            if score > 0:
                scored.append(dict(chunk, score=round(score, 5),
                                   repeats_claim=bool(exclude_text and norm(exclude_text).lower() in norm(chunk['text']).lower())))
        scored.sort(key=lambda c: (-c['score'], c['pdf_page'], c['chunk_id']))
        # A repeated claim is shown as context, never automatically treated as proof.
        return scored[:k]

def process_all():
    manifest = load_json(DATA/'manifest.json', [])
    candidates, stats = [], []
    for report in manifest:
        if report.get('status') not in ('downloaded','processed'):
            continue
        cache = DATA/'processed'/f"{report['report_id']}.json"
        parsed = load_json(cache)
        if not parsed or parsed.get('version') != VERSION or parsed['report'].get('sha256') != report.get('sha256'):
            parsed = parse_pdf(ROOT/report['pdf_path'],report)
            save_json(cache, parsed)
        claims = baseline_candidates(parsed)
        candidates.extend(claims)
        stats.append(dict(report_id=report['report_id'], company=report['company'],
                          year=report['report_year'], split=report['split'],
                          pages=len(parsed['pages']), chunks=len(parsed['chunks']),
                          relevant_pages=sum(p['packaging_relevant'] for p in parsed['pages']),
                          low_text_pages=sum(p['needs_ocr'] for p in parsed['pages']),
                          candidate_count=len(claims)))
        print(report['report_id'], len(parsed['pages']), 'pages;', len(claims), 'candidates', flush=True)
    save_json(DATA/'candidates.json', candidates)
    save_json(DATA/'corpus_stats.json', stats)
    (DATA/'candidates.csv').write_text(csv_text(candidates), encoding='utf-8-sig')
    (DATA/'corpus_stats.csv').write_text(csv_text(stats), encoding='utf-8-sig')

if __name__ == '__main__':
    process_all()
