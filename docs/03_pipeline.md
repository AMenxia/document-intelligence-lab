# Pipeline

## 1. Upload + Template

The user uploads one or more PDFs and selects:

- analysis mode
- extraction template
- LLM model
- VLM model
- Ollama URL
- output folder

Supported analysis modes:

```text
Individual Document Analysis
Consolidated Dossier
```

## 2. Run Docling

Docling parses each document and creates the first set of outputs.

```text
raw_docling.md
raw_docling.json
outlined_file.pdf
layout_items.json
raw_tables.json
visual_items.json
crop previews
```

## 3. Document Item Review

The app displays the parsed document items in reading order.

The review view shows:

- item type
- page number
- raw preview
- crop preview when available
- quick skim result
- review status

Quick skim labels help identify low-information visual crops before running expensive model steps.

```text
likely_useful
likely_empty
likely_decorative
needs_review
```

## 4. LLM Table Correction

Docling extracts table content first. The text LLM corrects selected table outputs into structured rows and columns.

Output:

```text
cleaned_tables.json
```

## 5. Image / Chart VLM Review

Visual items can be reviewed before VLM analysis.

Each visual item can include:

- crop preview
- page number
- review status
- optional reviewer note
- VLM summary

Output:

```text
image_summaries.json
```

## 6. Build LLM Feed

The app rebuilds a clean Markdown feed from the document item sequence.

```text
text → copied
headers → headings
lists → list items
tables → cleaned table inserted
visuals → VLM summary inserted
```

Output:

```text
file_llm_feed.md
```

## 7. Analysis + Extraction

The selected template is applied to the cleaned document feed.

Outputs:

```text
structured_extraction.json
final_report.md
consolidated_dossier.json
consolidated_dossier.md
```

## 8. Excel Preview + Download

The app creates an Excel workbook and displays preview tables before download.

Common sheets:

```text
overview
documents
layout_items
raw_tables
cleaned_tables
visual_items
image_summaries
field_values
conflicts_or_notes
```
