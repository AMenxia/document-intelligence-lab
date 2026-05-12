# Phases

## Phase 0 — Intake + Mode Selection
Choose an analysis mode:

```text
Individual Document Analysis
Consolidated Dossier
```

Then choose one extraction template for the run.

## Phase 1 — Docling Parse
Run Docling on each file and export Markdown, JSON, layout boxes, and outlined PDFs.

## Phase 2 — Crop Generation
Crop table/image/picture regions from detected layout boxes.

## Phase 3 — Human Crop Review
Mark crops as keep, discard, or needs_review.

## Phase 4 — Optional Table Cleanup
Run a vision-capable model on selected table crops and produce:

```text
cleaned_tables.json
```

## Phase 5 — Optional VLM Crop Summaries
Run the selected VLM on kept/needs_review crops and produce:

```text
vlm_results.json
```

## Phase 6 — Analysis

### Individual Document Analysis

Each document gets its own structured extraction.

```text
doc_001/structured_extraction.json
doc_002/structured_extraction.json
individual_analyses.json
```

### Consolidated Dossier

Each document is extracted first, then all document results are merged into one dossier.

```text
individual_analyses.json
consolidated_dossier.json
consolidated_dossier.md
```

## Phase 7 — Excel Export
Preview workbook sheets in Streamlit and download a formatted `.xlsx` file.

Possible sheets:

```text
overview
documents
field_values
people_or_entities
visual_evidence
cleaned_tables
conflicts_or_notes
```
