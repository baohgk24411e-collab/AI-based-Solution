"""Download the curated corpus; discover extra PDF links without automatically selecting them."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from io import BytesIO
import urllib.request
from urllib.parse import urljoin, urlparse

from pypdf import PdfReader
from .common import DATA, save_json, load_json, digest, csv_text

UA = 'Mozilla/5.0 (compatible; GreenClaimStudentResearch/1.0)'
MAX_BYTES = 80 * 1024 * 1024

def get_url(url):
    if urlparse(url).scheme != 'https':
        raise ValueError('Only HTTPS public report URLs are supported')
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as response:
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError('File exceeds 80 MB limit')
        return body, response.url

def download_one(row):
    row = dict(row)
    path = DATA / 'raw_pdfs' / (row['report_id'] + '.pdf')
    try:
        if path.exists():
            body, final_url = path.read_bytes(), row['source_url']
        else:
            body, final_url = get_url(row['source_url'])
        if not body.startswith(b'%PDF-'):
            raise ValueError('Response is not a PDF')
        reader = PdfReader(BytesIO(body))
        if reader.is_encrypted and not reader.decrypt(''):
            raise ValueError('Password-protected PDF')
        pages = len(reader.pages)
        if not pages:
            raise ValueError('Empty PDF')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
        row.update(status='downloaded', page_count=pages, byte_count=len(body),
                   sha256=digest(body), pdf_path=str(path.relative_to(DATA.parent)),
                   resolved_url=final_url, error='', retrieved_at=datetime.now(timezone.utc).isoformat())
    except Exception as exc:
        row.update(status='download_failed', error=str(exc))
    print(row['report_id'], row['status'], row.get('page_count', ''), row.get('error', ''), flush=True)
    return row

def collect():
    rows = load_json(DATA / 'sources.json', [])
    with ThreadPoolExecutor(max_workers=3) as pool:
        result = list(pool.map(download_one, rows))
    seen = {}
    for row in result:
        sha = row.get('sha256')
        if sha and sha in seen:
            row.update(status='duplicate', duplicate_of=seen[sha])
        elif sha:
            seen[sha] = row['report_id']
    save_json(DATA / 'manifest.json', result)
    (DATA / 'manifest.csv').write_text(csv_text(result), encoding='utf-8-sig')

def discover(url):
    class Links(HTMLParser):
        def __init__(self):
            super().__init__()
            self.links = set()
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if tag == 'a' and key == 'href' and value and '.pdf' in value.lower():
                    self.links.add(urljoin(url, value))
    body, final = get_url(url)
    parser = Links()
    parser.feed(body.decode('utf-8', errors='replace'))
    return sorted(parser.links)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--discover', help='Official company report landing page')
    args = parser.parse_args()
    if args.discover:
        print('\n'.join(discover(args.discover)))
    else:
        collect()
