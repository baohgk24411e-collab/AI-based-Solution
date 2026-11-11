# Pipeline Limitations & Engineering Constraints

## 1. PDF Text Extraction & Structural Layout Boundaries
* **Pure Text Stream (No OCR):** The ingestion pipeline relies on `pypdf` stream extraction. Documents containing scanned images, rasterized text, or complex infographic banners without text layers cannot be extracted without an OCR subsystem (e.g., Tesseract/PaddleOCR).
* **Multi-Column Tables & Layout Disruption:** Sustainability reports often present metrics in multi-column tables. Linear PDF text extraction can flatten rows into ambiguous sequences, occasionally causing LLMs to associate metric values with adjacent row headers or neighboring years.
* **Page Indexing vs. Printed Folios:** Physical PDF page indices (1-indexed) frequently diverge from printed publication folios due to front-matter, cover pages, and Roman numeral numbering.

## 2. Evidence Retrieval (BM25 Lexical Scope)
* **Intra-Report Retrieval:** Current evidence retrieval is strictly scoped within the same report ID. Cross-year comparative analysis (e.g., comparing 2021 baseline vs. 2024 claimed achievement across different annual publications) is not autonomously linked in this single-report retrieval pass.
* **Lexical vs. Semantic Embedding:** BM25 matching prioritizes keyword frequencies. Claims utilizing heavy paraphrase or corporate euphemisms without overlapping packaging keywords may experience lower retrieval recall than dense semantic vector embeddings.

## 3. LLM Extraction & Assessment Hallucination Patterns
* **Neighboring Table Cell Confusion (12.7% Metric Error Rate):** When extracting quantitative fields (`value`, `unit`, `target_year`), small local models (e.g., 7B parameters) occasionally pick up progress percentages from adjacent table rows rather than the target percentage stated in the sentence.
* **Implicit Verbal Deduction:** Phrases like *"halve our virgin plastics"* are occasionally converted into numeric `50%` by the LLM even though the digit `50` does not literally appear in the sentence.
* **Documentary Support vs. Factual Truth:** A verdict of `supported` exclusively denotes that the cited report text contains matching claims and documentary substantiation. It does **not** constitute independent forensic auditing or external physical verification of corporate practices.

## 4. Greenwashing Detection Scope
* **Report-Internal Consistency:** The system flags internal discrepancies (e.g., future commitments presented as achieved, lack of baseline years, scope mismatch between plastic vs. all packaging). It cannot detect supply-chain fraud, unrecorded waste exports, or off-balance-sheet environmental impacts occurring outside official corporate filings.
