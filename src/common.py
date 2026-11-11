import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'

def load_json(path, default=None):
    return json.loads(Path(path).read_text(encoding='utf-8')) if Path(path).exists() else default

def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)

def digest(value):
    if not isinstance(value, bytes):
        value = json.dumps(value, sort_keys=True, ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(value).hexdigest()

def csv_text(rows, fields=None):
    import io
    out = io.StringIO(newline='')
    fields = fields or list(dict.fromkeys(k for r in rows for k in r))
    writer = csv.DictWriter(out, fields, extrasaction='ignore')
    writer.writeheader()
    for row in rows:
        safe = {}
        for k, v in row.items():
            v = json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v
            # Prevent spreadsheet formulas when a report's text is exported.
            if isinstance(v, str) and v.startswith(('=', '+', '-', '@')):
                v = "'" + v
            safe[k] = v
        writer.writerow(safe)
    return out.getvalue()
