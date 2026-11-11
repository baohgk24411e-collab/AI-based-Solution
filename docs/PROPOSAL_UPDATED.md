# An explainable AI system for reviewing plastic packaging claims in FMCG reports

Group 10

Course: AI Based Solution in Business and Management, 261EIM500601  
Lecturer: Ph.D. Trinh Quang Viet  
Implementation update: 11 November 2026

## Project objective

This project develops a local research application that helps reviewers examine plastic packaging claims in corporate sustainability disclosures. The system identifies candidate claims, retrieves relevant passages, compares claims with documentary evidence using an LLM, and records source references for human review. A separate Python component recalculates percentages when a reviewer confirms that the underlying quantities are comparable.

The intended users are students, ESG researchers and sustainability analysts who need to locate supporting information efficiently. The system assesses documentary support and consistency within the available report. It does not establish whether a company engaged in greenwashing, and it does not independently verify conditions outside the documents.

## Research questions

1. How reliably can a structured LLM prompt identify plastic packaging claims in selected report pages?
2. How often does BM25 retrieve the pages a human reviewer identifies as relevant evidence?
3. How closely do evidence-grounded LLM assessments agree with adjudicated human labels?
4. Which errors arise from PDF extraction, retrieval, scope interpretation and numerical comparisons?

## Corpus and selection

The implemented corpus contains 20 English-language PDF reports from five FMCG companies. The files were downloaded from official corporate websites or asset hosts directly linked by those websites. Each file has a report ID, company, reporting year, source URL, discovery URL, PDF page count, download timestamp and SHA-256 checksum.

| Company | Reporting years | Documents | Document type |
|---|---|---:|---|
| Nestlé | 2021–2024 | 4 | Creating Shared Value and sustainability reports |
| Danone | 2021–2024 | 4 | Universal Registration Documents containing environmental disclosures |
| Procter & Gamble | 2021–2024 | 4 | Citizenship reports and the 2024 data and metrics summary |
| Reckitt | 2021–2024 | 4 | Sustainability reports and sustainability insights |
| The Coca-Cola Company | 2022–2025 | 4 | Business and sustainability report and environmental updates |

The selection is purposive rather than statistically representative. Relevant packaging content and readable PDF text are the primary inclusion criteria. Different document types and lengths remain a source of variation. P&G reports for 2021 and 2024 contain relatively few candidate passages, so claim counts will not be balanced across companies. The 2025 Coca-Cola update was published in 2026 and is available as of this implementation date.

Initial PepsiCo and Unilever download attempts returned HTTP 403. The final corpus substitutes P&G and Reckitt, and the collection log retains the unsuccessful attempts. A missing Coca-Cola 2021 URL was replaced with its official 2025 environmental update. Sources and exclusions are recorded rather than silently omitted.

The corpus has 2,565 PDF pages and 4,930 searchable chunks. A broad packaging and recycling keyword filter identifies 389 pages and produces 1,026 unverified candidate passages. These counts describe preprocessing output, not validated environmental claims or model performance. Thirty-seven pages have fewer than 60 normalized text characters and are flagged for inspection. They may be image-only pages, covers or intentionally sparse pages.

## Scope of claims

The analysis covers recyclability, recycled content, collection or recycling performance, and future commitments concerning plastic packaging. Composite metrics such as reusable, recyclable or compostable packaging retain their original definition. All-packaging metrics may be included when they cover plastics, but the system must not interpret them as plastic-only metrics.

Each extracted claim records its original text, source PDF page, type, company, reporting year, measurement year when available, target year, material, scope, numerical value and unit. Missing attributes remain unknown. The report year does not automatically define the period of every numerical statement.

## Implemented workflow

### Document collection

A Python downloader retrieves the curated source list, verifies the PDF signature and readability, records checksums and identifies exact duplicate files. A discovery command can list PDF links on an official report landing page. The current implementation uses reviewed source selection rather than unrestricted autonomous crawling.

### Preprocessing

pypdf extracts text by physical PDF page. The pipeline retains the whole page and creates normalized chunks of up to 2,500 characters with 400-character overlap. Page references and report metadata accompany every chunk. A low-text flag identifies pages that may require additional inspection.

The current prototype does not perform OCR, chart interpretation or structured reconstruction of multi-column tables. Reviewers must inspect the original PDF before using ambiguous table values. PDF page indices are one-based and may differ from printed page numbers.

### Baseline extraction and retrieval

A keyword baseline identifies candidate passages containing packaging/material vocabulary and recycling-related terms. Its labels are type suggestions only. The baseline can include irrelevant headings, broad policy language, non-plastic packaging or incomplete table passages. These errors must be measured and reviewed.

BM25 ranks chunks from the same report for a selected claim or reviewer-entered query. The default returns five chunks. Chunks containing the original claim are explicitly marked as repeating the claim because repetition is not independent substantiation. Cross-year and external-source retrieval are outside the current implementation.

### LLM extraction and verification

The Gemini REST adapter supports two operations. First, it extracts claims into structured JSON from selected pages. Second, it compares a claim with retrieved evidence and returns an assessment, rationale, flags and exact citations. The application checks that quoted text occurs on the cited page/chunk and rejects malformed or ungrounded output.

Prompts distinguish actual recycling from recyclability, collection and recycled content. They require compatible periods and scope, preserve uncertainty and treat report text as evidence rather than instructions. The UI limits extraction to one to three pages per operation. The batch runner has an explicit maximum-call limit and records processed pages. A cache is keyed by model, prompt version and input content. Token usage and timing are stored when a live API response is available.

The model ID is configurable. No fine-tuning or local model hosting is required. A live API key is required to execute the LLM component. The current handover includes the integration but does not claim live model results.

### Assessment labels

| Label | Interpretation |
|---|---|
| Supported | The supplied documentary evidence supports the claim within the evaluated scope |
| Insufficient evidence | The inspected evidence is insufficient to assess the claim |
| Scope mismatch | The available evidence concerns a different period, material, geography or boundary |
| Potential inconsistency | Comparable documentary information conflicts and requires review |
| Not yet assessable | Achievement of a future target cannot be assessed from the earlier reporting period |

The fifth label resolves a temporal issue in the original mockup. A future target in an earlier report cannot be treated as an unfulfilled claim merely because completion data are not yet available. Supported denotes documentary support and does not establish external truth.

### Numerical checks

The arithmetic component requires a nonnegative numerator, positive denominator, supported mass units and compatible company, period, material, geography, boundary and measurement basis. It normalizes kilograms and tonnes, recalculates the percentage and reports the difference in percentage points. The default tolerance is 0.5 percentage points and should be reconsidered when source rounding differs.

The UI accepts quantities transcribed and checked by a reviewer. It does not automatically infer numerical values or denominators from PDF tables. A successful arithmetic check does not validate the underlying corporate data.

## Evaluation design

The corpus is divided into 10 development reports and 10 test reports. For Nestlé, Danone, P&G and Reckitt, 2021–2022 are development and 2023–2024 are test. For Coca-Cola, 2022–2023 are development and 2024–2025 are test. This split measures later-period performance within known companies, not generalization to unseen companies. Similar wording across years may still make the task easier and must be discussed.

Human reviewers will identify relevant claims and supporting pages, assign labels independently for a cross-checked subset, and adjudicate disagreements. The provided 114-item review queue prioritizes concise quantitative candidates for workflow testing. It is not a random sample or an exhaustive gold dataset.

Claim extraction precision, recall and F1 require exhaustive reference annotation within the evaluated sections and a documented matching policy. Retrieval evaluation will use page-level Recall@k and Hit@k. Verification evaluation will report accuracy, a confusion matrix and macro-F1 on adjudicated test claims with saved predictions. The implemented evaluator explicitly reports this conditional coverage and the labels included in macro-F1. It does not substitute this metric for end-to-end performance.

No human gold labels or live LLM predictions were available at implementation handover. Therefore model accuracy, extraction recall and verification F1 remain unmeasured. Software tests assess implementation behavior, not model quality.

## Deliverables and present status

The delivered package contains the downloaded corpus, source manifest, page text, searchable chunks, candidate dataset, annotation queue, Python modules, Streamlit application, prompts, tests and operating documentation. The local application supports uploading additional readable PDFs, browsing the corpus, finding evidence, saving human reviews, calling the configured LLM, checking percentages and exporting results.

Remaining empirical work consists of API configuration, prompt trials on development reports, human annotation, adjudication and a fixed test run. The final analytical report must distinguish observed results from implementation descriptions and planned evaluation.

## Limitations and business value

The prototype can reduce navigation effort by placing a candidate claim and relevant source passages together. It can also expose differences in denominators or scope that deserve attention. Time savings and user value have not yet been measured in a user study.

The key limitations are imperfect PDF text order, keyword filtering errors, limited lexical retrieval, missing external evidence, potential LLM reasoning errors and an unbalanced purposive corpus. Exact quote checking provides traceability but does not guarantee correct inference. The application is a local single-user research prototype without production authentication or multi-user concurrency controls.

## Sources

- Nestlé report archive: https://www.nestle.co.jp/csv/downloads
- Danone reports: https://www.danone.com/investors/publications-and-events/financial-and-extra-financial-reports.html
- P&G report archive: https://us.pg.com/sustainability-reports/
- Reckitt archive: https://www.reckitt.com/our-impact/reporting-hub/reporting-hub-archive/
- Coca-Cola sustainability disclosures: https://www.coca-colacompany.com/policies-and-practices/sustainability
- Exact document URLs, checksums and download metadata: data/manifest.csv
- Gemini API documentation: https://ai.google.dev/api/generate-content
