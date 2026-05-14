# Output Files

## Run folder

Each processing run creates a timestamped folder.

```text
runs/
  run_YYYYMMDD_HHMMSS/
```

## Per-document outputs

```text
doc_001/
  source.pdf
  raw_docling.md
  raw_docling.json
  outlined_file.pdf
  layout_items.json
  raw_tables.json
  cleaned_tables.json
  visual_items.json
  image_summaries.json
  file_llm_feed.md
  structured_extraction.json
  final_report.md
```

## Consolidated outputs

When consolidated dossier mode is used, the run can also include:

```text
consolidated/
  consolidated_dossier.json
  consolidated_dossier.md
  workbook.xlsx
```

## Output descriptions

| Output | Description |
|---|---|
| `raw_docling.md` | Raw Markdown export from Docling |
| `raw_docling.json` | Raw structured export from Docling |
| `outlined_file.pdf` | PDF preview with detected layout boxes |
| `layout_items.json` | Ordered item-level document map |
| `raw_tables.json` | Tables extracted from Docling |
| `cleaned_tables.json` | LLM-corrected table structures |
| `visual_items.json` | Visual item/crop manifest |
| `image_summaries.json` | VLM summaries for selected visuals |
| `file_llm_feed.md` | Clean document feed used for final extraction |
| `structured_extraction.json` | Template-based extraction output |
| `final_report.md` | Human-readable report |
| `workbook.xlsx` | Excel export |
