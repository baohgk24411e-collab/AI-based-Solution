import glob, json, re
from src.common import DATA, load_json
from src.pipeline import norm

claims_files = glob.glob('data/llm_claims/*.json')
val_mismatch = []
val_match = []
total_claims = 0

for cf in claims_files:
    data = load_json(cf, {})
    rid = cf.split('\\')[-1].replace('.json', '')
    for c in data.get('claims', []):
        total_claims += 1
        val = c.get('value')
        txt = c.get('claim_text', '')
        if val is not None:
            # find all numbers in txt (including comma-formatted)
            nums_in_txt = re.findall(r'\d[\d,]*(?:\.\d+)?', txt)
            floats_in_txt = [float(n.replace(',', '')) for n in nums_in_txt]
            try:
                val_float = float(val)
                if any(abs(val_float - f) < 1e-4 for f in floats_in_txt):
                    val_match.append((rid, c['claim_id'], val, c.get('unit'), txt))
                else:
                    val_mismatch.append((rid, c['claim_id'], val, floats_in_txt, txt))
            except (ValueError, TypeError):
                val_mismatch.append((rid, c['claim_id'], val, floats_in_txt, txt))

print(f"Tổng số claims đã trích xuất: {total_claims}")
print(f"Tổng số claims có metric số liệu: {len(val_match) + len(val_mismatch)}")
print(f"Metrics trích xuất CHÍNH XÁC (không hallucination): {len(val_match)} ({len(val_match)/(len(val_match)+len(val_mismatch))*100:.2f}%)")
print(f"Metrics bị SAI LỆCH / HALLUCINATION số liệu: {len(val_mismatch)} ({len(val_mismatch)/(len(val_match)+len(val_mismatch))*100:.2f}%)")

print("\n--- CÁC VÍ DỤ METRIC BỊ HALLUCINATION / NHẦM LẪN SỐ ---")
for r, cid, val, in_txt, txt in val_mismatch[:5]:
    print(f"• Báo cáo [{r}] (ID: {cid}):")
    print(f"  - Đoạn gốc PDF: \"{txt.strip()}\"")
    print(f"  - LLM trích xuất value = {val}, trong khi các số thực tế trong câu là: {in_txt}")

print("\n--- CÁC VÍ DỤ METRIC CHÍNH XÁC TUYỆT ĐỐI (GROUNDED 100%) ---")
for r, cid, val, unit, txt in val_match[:6]:
    print(f"• Báo cáo [{r}] (ID: {cid}):")
    print(f"  - Đoạn gốc PDF: \"{txt.strip()}\"")
    print(f"  - Metric trích xuất: {val} {unit or ''} (Khớp chính xác với số liệu văn bản)")

