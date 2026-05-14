# Future Work

## Planned improvements

Potential improvements include:

- embedding/vector search over cleaned document feeds
- semantic table lines for retrieval
- VLM fallback for severely broken tables
- table validation rules
- extraction confidence scoring
- richer source citation tracking
- better OCR options for scanned PDFs
- batch processing queue
- manual layout correction tools
- automated test documents
- extraction quality evaluation reports

## Table pipeline improvements

Future table correction can add:

- validation against raw Docling output
- row/column count checks
- source-cell tracing
- model retry logic
- side-by-side raw vs. cleaned comparison

## Visual pipeline improvements

Future visual review can add:

- image type classification
- chart-specific prompts
- diagram-specific prompts
- OCR text extraction from images
- visual importance scoring
- VLM fallback comparison across models

## Retrieval improvements

A future retrieval phase can use:

```text
file_llm_feed.md
cleaned_tables.json
image_summaries.json
```

Then create searchable chunks with metadata:

```text
doc_id
source file
page number
item ID
item type
```
