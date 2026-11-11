# System Architecture & AI Pipeline

```
+-----------------------------------------------------------------------------------+
|                            GREENCLAIM AI ARCHITECTURE                             |
+-----------------------------------------------------------------------------------+
                                         │
 1. DATA INGESTION                       ▼
    [ Corporate PDFs (20 files) ] ──> [ pypdf Stream Extractor ]
                                         │
 2. TEXT PROCESSING                      ▼
    [ Physical Page Indexing ] ──> [ Character Chunks (2500 chars, 400 overlap) ]
                                         │
 3. LEXICAL PRE-FILTER                   ▼
    [ Packaging & Recycling Keywords ] ──> [ 389 Relevant Pages Identified ]
                                         │
 4. STRUCTURED LLM EXTRACTION            ▼
    [ Local LM Studio (Qwen 2.5 7B) / Gemini ] ──> Strict JSON Schema Enforcement
                                         │
                                         ├──> [ Exact Quote Verification: 100% Grounded ]
                                         └──> [ Extracted 631 Claims with Metadata ]
                                         │
 5. EVIDENCE RETRIEVAL                   ▼
    [ BM25 Full-Report Inverted Index ] ──> [ Top-K Candidate Chunks per Claim ]
                                         │
 6. MULTI-STEP VERIFICATION & AUDIT      ▼
    [ LLM Citation & Rationale Agent ] ──> [ Exact Substring Quote Validation ]
                                         │
                                         ├──> Passed: Saved to Assessment Registry
                                         └──> Mismatched Quote: Repair Loop or Rejected
                                         │
 7. USER INTERFACE & REPORTING           ▼
    [ Streamlit Research Workbench ] <── [ summary.json / claims_and_assessments.csv ]
```

## Pipeline Execution Stages
1. **Document Ingestion:** Reads 20 official English PDF reports from Nestlé, Danone, Coca-Cola, P&G, and Reckitt.
2. **Chunking & Indexing:** Tokenizes and indexes text into 4,930 searchable passages with exact page tracking.
3. **Keyword Filtering:** Filters 2,565 total pages down to 389 packaging-relevant candidate pages to conserve compute.
4. **LLM Claim Extraction:** Prompts the model with strict JSON schema to parse:
   * `claim_text`: Exact verbatim quotation from the text.
   * `claim_type`: `target`, `recyclability`, `recycled_content`, `collection_recycling`.
   * Quantitative metadata: `value`, `unit`, `target_year`, `measurement_year`.
5. **Exact Substring Gatekeeper:** Validates that `claim_text` exists literally on the cited PDF page. Any fabricated or altered quotation is immediately discarded.
6. **BM25 Evidence Retrieval:** Performs keyword-driven document retrieval for each claim across the entire publication to retrieve corresponding disclosures, definitions, or conflicting footnotes.
7. **Adjudication & Verification:** Compares the claim against evidence chunks, producing labels:
   * `supported`: Substantive corroborating evidence found in the document.
   * `insufficient_evidence`: Broad statements or metrics lacking methodology or baseline context.
   * `scope_mismatch`: Plastic claims mixed with paper, glass, or non-packaging scopes.
   * `potential_inconsistency`: Conflicting figures across different sections or years.
   * `not_yet_assessable`: Future commitments that have not matured.

