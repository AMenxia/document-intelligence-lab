# Streamlit Usage

## Start the app

From the project root:

```bash
streamlit run app/streamlit_app.py
```

Or use the included Windows batch file:

```bash
run_app.bat
```

## Sidebar controls

The sidebar contains:

```text
Analysis Mode
Template
LLM Model
VLM Model
Ollama URL
Runs Directory
```

## Typical workflow

1. Upload one or more PDFs.
2. Select an extraction template.
3. Select individual or consolidated analysis mode.
4. Run Docling.
5. Review detected document items.
6. Correct selected tables with the text LLM.
7. Review visual crops and add optional reviewer notes.
8. Run VLM review on selected visuals.
9. Build the LLM feed.
10. Run analysis/extraction.
11. Preview and download Excel outputs.

## Individual Document Analysis

Each document is analyzed separately.

Example outputs:

```text
doc_001/structured_extraction.json
doc_001/final_report.md
doc_002/structured_extraction.json
doc_002/final_report.md
```

## Consolidated Dossier

Multiple documents are merged into a combined report.

Example outputs:

```text
consolidated_dossier.json
consolidated_dossier.md
workbook.xlsx
```
