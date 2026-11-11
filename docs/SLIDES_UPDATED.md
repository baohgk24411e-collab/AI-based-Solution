# Slide content and speaker notes

This is editable slide copy for an implementation update. It replaces proposed corpus descriptions with actual preprocessing counts and retains an explicit distinction between implemented software and unmeasured model performance.

## 1 GreenClaim

Explainable review of plastic packaging claims in FMCG reports

Group 10  
AI Based Solution in Business and Management  
261EIM500601

Speaker note: Explain that the system assists document review and does not issue definitive greenwashing findings.

## 2 Problem and scope

- Packaging claims use different periods, materials and reporting boundaries.
- Reviewers need the original claim, supporting passages and definitions together.
- Scope: recyclability, recycled content, collection/recycling performance and future targets.

Speaker note: Distinguish a claim about design from a claim about actual recycling. A composite reusable/recyclable/compostable metric is not a recyclability-only measure.

## 3 Collected corpus

20 reports from 5 FMCG companies

| Company | Years | Reports |
|---|---|---:|
| Nestlé | 2021–2024 | 4 |
| Danone | 2021–2024 | 4 |
| P&G | 2021–2024 | 4 |
| Reckitt | 2021–2024 | 4 |
| Coca-Cola | 2022–2025 | 4 |

Sources: official company report archives and their linked asset hosts.

Speaker note: Use data/manifest.csv for exact links. P&G/Reckitt replaced sources that returned HTTP 403. This is a purposive sample, not representative of the FMCG industry.

## 4 What the crawler collects

Reviewed source pages and PDF links

PDF download and validity check

Company, report year, URL, page count and SHA-256

Output: 20 original PDFs and a traceable manifest

Speaker note: The crawler handles document acquisition. The LLM handles extraction and comparison. The downloader detects exact duplicate files.

## 5 Preprocessing results

2,565 PDF pages  
4,930 searchable chunks  
389 pages matched the packaging keyword filter  
1,026 unverified candidate passages

Whole-page text and PDF page references remain available.

Speaker note: These are software output counts, not verified claims or model accuracy. The parser flags 37 low-text pages. OCR and automatic table reconstruction are not implemented.

## 6 LLM extraction

Input: selected report pages with company, year and PDF page IDs

Output fields:

- Exact claim text and claim type
- Scope, material, measurement year and target year when stated
- Value, unit and original page

Exact-source validation rejects invented quotations and wrong page references.

Speaker note: Missing fields remain unknown. Live Gemini execution requires an API key and a selected model ID. The current package does not contain fabricated API results.

## 7 Evidence retrieval and assessment

Claim selection

BM25 retrieval within the same report

LLM comparison of meaning, period, scope and evidence

Output: label, rationale, evidence quotations and page IDs

Speaker note: The default retrieves five chunks. Repeating a claim is not independent substantiation. Exact quote matching checks location, not the correctness of the model's reasoning.

## 8 Assessment labels

| Label | Meaning |
|---|---|
| Supported | Evidence supports the claim within the evaluated scope |
| Insufficient evidence | Available evidence does not resolve the claim |
| Scope mismatch | Claim and evidence concern different boundaries |
| Potential inconsistency | Comparable evidence conflicts |
| Not yet assessable | Future achievement cannot be judged from an earlier period |

Speaker note: The fifth label fixes the original future-target example. Absence of achievement data before a deadline must not be interpreted as a failed target.

## 9 Numerical validation

Python checks percentages after the reviewer confirms comparability.

Illustrative arithmetic, not company data:

2,500 / 10,000 = 25%  
2,500 / 4,000 = 62.5%

The denominator changes the meaning of the rate.

Speaker note: Units, reporting period, material, geography and operational boundary must match. Current UI requires manually checked source numbers and does not infer them automatically from tables.

## 10 Local prototype

Five work areas:

1. Corpus and exports
2. Claim candidates and source passages
3. LLM extraction and verification
4. Arithmetic checks
5. Human-reference evaluation

CPU for PDF parsing and retrieval. API for LLM inference.

Speaker note: Open the running Streamlit application and follow docs/DEMO_SCRIPT.md. Without an API key, demonstrate the baseline and explain which functions remain unexecuted.

## 11 Evaluation design

10 development reports and 10 test reports

Human annotation and cross-checking before model scoring

Extraction: precision, recall and F1 after exhaustive reference annotation  
Retrieval: page Recall@k and Hit@k  
Verification: macro-F1 and confusion matrix

Speaker note: Later-year test reports belong to companies seen in development. The 114-item review queue is a workflow starting point, not an exhaustive or representative gold standard.

## 12 Current status

Implemented: corpus, parser, baseline, retrieval, LLM adapter, source validation, numeric checks and local UI.

Pending: live API execution, independent human labels and model performance measurement.

Next empirical step: annotate development claims, freeze prompts and evaluate the held-out reports.

Speaker note: Do not replace pending results with invented accuracy. Functional software tests are separate from research evaluation.
