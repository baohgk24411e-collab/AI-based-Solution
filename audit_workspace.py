from pathlib import Path
from pypdf import PdfReader
from src.common import DATA,ROOT,load_json,save_json,digest
inventory=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or any(x in ('.git','.venv','__pycache__','cache','assessments','llm_claims','results','run_archive') for x in p.relative_to(ROOT).parts):
        continue
    row={'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size}
    if p.suffix in ('.py','.md','.toml','.ps1','.cmd','.txt','.json','.csv'):
        text=p.read_text(encoding='utf-8-sig')
        row['lines']=len(text.splitlines())
        if p.suffix=='.json':
            import json
            row['json_valid']=True
            value=json.loads(text)
            row['items']=len(value) if isinstance(value,(list,dict)) else None
    if p.suffix=='.pdf':
        reader=PdfReader(p)
        if reader.is_encrypted:
            reader.decrypt('')
        row['pdf_pages']=len(reader.pages)
        row['sha256']=digest(p.read_bytes())
        if 'original' in p.parts:
            print(p.name)
            print('\n'.join((page.extract_text() or '') for page in reader.pages)[:24000])
    inventory.append(row)
save_json(DATA/'file_inventory.json',inventory)
print('Inventory files:',len(inventory))
