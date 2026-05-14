# Document Intelligence Lab

A Streamlit demo for building a **DoclingDocument-centered document intelligence pipeline**.

This project treats Docling's structured document output as the center of the workflow instead of treating exported Markdown as the main source. The app parses PDFs with Docling, creates a reading-order item manifest, routes tables to a text LLM for structured table correction, routes images/charts to a VLM with optional reviewer notes, rebuilds an LLM-friendly Markdown feed, and exports structured JSON/Excel reports.

## Core idea

```text
PDF upload
↓
Docling parses the PDF
↓
DoclingDocument becomes the source map
↓
layout_items.json records text/table/picture items in reading order
↓
raw table items → text LLM correction → cleaned_tables.json
↓
visual items → human notes + VLM review → image_summaries.json
↓
file_llm_feed.md is rebuilt from the corrected item sequence
↓
structured_extraction.json / report.md / Excel workbook
```

## What this demo shows

- DoclingDocument-driven parsing
- Reading-order layout item manifest
- Table crop previews for human verification
- Image/chart crop previews for human review
- Quick skim labels for mostly blank/decorative crops
- LLM table correction into structured rows + columns
- Optional human context notes before VLM image/chart review
- Individual document analysis or consolidated dossier mode
- Excel preview and export

## Project structure

```text
document-intelligence-lab/
  app/
    streamlit_app.py
  src/docintellab/
    config.py
    docling_pipeline.py
    quick_skim.py
    ollama_client.py
    table_corrector.py
    visual_analyzer.py
    feed_builder.py
    extraction.py
    excel_exporter.py
    templates.py
    utils.py
  templates/
    generic_document.json
    research_paper.json
    grant_program.json
    event_flyer.json
    company_overview_public.json
  data/
    sample_docs/
      README.md
    private/
      README.md
  demo_outputs/
    README.md
  assets/screenshots/
    README.md
  requirements.txt
  .env.example
  .gitignore
  run_app.bat
```

## Setup

```bash
conda create -n docintellab python=3.11 -y
conda activate docintellab
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update paths/models if needed.

```bash
cp .env.example .env
```

On Windows, you can also copy the file manually.

## Run

```bash
streamlit run app/streamlit_app.py
```

Or double-click/run:

```bash
run_app.bat
```

## Ollama models

Default model names are configurable in the app sidebar and `.env.example`.

Recommended local defaults:

```text
LLM_MODEL=qwen3:14b
VLM_MODEL=llama3.2-vision:latest
OLLAMA_URL=http://localhost:11434
```

Pull models with:

```bash
ollama pull qwen3:14b
ollama pull llama3.2-vision:latest
```

