# Architecture

## DoclingDocument-centered design

The pipeline is centered around Docling's structured document output.

```text
PDF
↓
Docling
↓
DoclingDocument
↓
ordered document items
↓
specialized processing steps
```

The app uses the parsed document structure to create an item-level map of each source document.

## Document item map

Each item can include:

- item ID
- document ID
- item type
- reading order index
- page number
- bounding box
- coordinate origin
- raw text preview
- raw table preview
- crop path when available
- review status

The generated item map is saved as:

```text
layout_items.json
```

## Item routing

```text
Text item
→ copied into file_llm_feed.md

Section header
→ written as a Markdown heading

List item
→ written as a list entry

Table item
→ exported from Docling
→ corrected with a text LLM
→ saved as structured rows and columns

Picture / chart / figure item
→ shown as a visual crop
→ optional reviewer note is added
→ analyzed with a VLM
→ saved as an image summary
```

## Sidecar outputs

Corrections and review outputs are stored separately from the raw parse.

```text
raw_tables.json
cleaned_tables.json
visual_items.json
image_summaries.json
file_llm_feed.md
```

This keeps raw parsing, human review, model correction, and final extraction outputs separate.
