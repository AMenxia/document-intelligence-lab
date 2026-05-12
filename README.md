# Document Intelligence Lab — Long Demo

A long-form document intelligence demo for template-based document analysis.

This project shows a practical workflow for turning public PDFs and document packets into structured JSON, Markdown reports, and Excel exports.

## What this app does

```text
Choose an analysis mode
Choose an extraction template
Upload one or more documents
Run Docling parsing
Generate Markdown, JSON, layout boxes, and outlined PDFs
Generate table/image crops
Human-review useful crops
Optionally clean selected table crops with a VLM
Optionally run VLM summaries on selected crops
Run template-based LLM analysis
Generate structured_extraction.json
Generate final_report.md or consolidated_dossier.md
Preview Excel sheets in Streamlit
Download formatted Excel workbook
```

## Analysis modes

```text
Individual Document Analysis
Consolidated Dossier
```

### Individual Document Analysis

Each uploaded document is analyzed separately.

Best for:

```text
research papers
event flyers
grant documents
generic PDFs
```

### Consolidated Dossier

All uploaded documents are analyzed as one packet. The app first extracts each document, then merges the results into one consolidated dossier.

Best for:

```text
company document packets
grant packets
research packets
multi-document business analysis
```

## Included templates

```text
generic_document
research_paper
grant_program
event_flyer
company_overview_public
```

Each run uses one selected template for all uploaded files.

## Default models

```text
VLM = llama3.2-vision:latest
LLM = deepseek-r1:8b
```

The VLM model is used for crop summaries and optional table cleanup because those steps look at crop images.

## Main outputs

```text
file.md
file.json
layout_boxes.json
outlined_file.pdf
crop_manifest.json
selected_crop_manifest.json
cleaned_tables.json
vlm_results.json
structured_extraction.json
individual_analyses.json
consolidated_dossier.json
final_report.md
consolidated_dossier.md
source-name_analysis.xlsx
source-name_dossier.xlsx
```

## Excel sheets

```text
overview
documents
field_values
people_or_entities
visual_evidence
cleaned_tables
conflicts_or_notes
```

The `conflicts_or_notes` sheet appears for Consolidated Dossier mode.

## Setup

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Optional Ollama setup:

```bash
ollama pull llama3.2-vision:latest
ollama pull deepseek-r1:8b
```


