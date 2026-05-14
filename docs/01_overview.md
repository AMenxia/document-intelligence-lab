# Project Overview

**Document Intelligence Lab** is a local-first document processing application for parsing PDFs, reviewing document elements, correcting table outputs, analyzing visuals, and exporting structured results.

The project uses:

- **Docling** for document parsing
- **Streamlit** for the user interface
- **Ollama-compatible LLMs** for structured extraction and table correction
- **Vision-language models** for image/chart review
- **JSON, Markdown, and Excel** for outputs

## Workflow

```text
PDF documents
↓
Docling parsing
↓
DoclingDocument item map
↓
document item review
↓
LLM table correction
↓
VLM image/chart review
↓
LLM-friendly document feed
↓
structured extraction
↓
JSON / Markdown / Excel outputs
```

## Core design

The project routes different document elements through different processing paths.

```text
text blocks → copied into the LLM feed
tables → corrected with a text LLM
images/charts → analyzed with a VLM
templates → guide structured extraction
```

This keeps the pipeline modular and makes each output easier to inspect.
