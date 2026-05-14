# LLM Table Correction

## Purpose

Docling can identify and extract tables, but table outputs may contain formatting issues from PDF structure, OCR, line wrapping, or merged cells.

The table correction phase converts Docling's table output into a cleaner structured format.

## Flow

```text
Docling TableItem
↓
raw Docling table output
↓
text LLM correction
↓
cleaned rows + columns
↓
Excel/report export
```

## Input

Each table correction request can include:

- source file name
- page number
- source item ID
- raw table Markdown
- raw table HTML/CSV when available
- nearby text when available

## Output

Each corrected table is saved as a structured JSON object.

```json
{
  "table_id": "doc_001_table_001",
  "doc_id": "doc_001",
  "source_item_id": "doc_001_item_0091",
  "file_name": "example.pdf",
  "page_no": 7,
  "caption": "",
  "columns": ["Column 1", "Column 2"],
  "rows": [
    {
      "Column 1": "value",
      "Column 2": "value"
    }
  ],
  "issues": []
}
```

## Correction rules

The table correction prompt instructs the model to:

- preserve numbers, dates, names, labels, and units
- avoid inventing missing values
- avoid summarizing the table
- repair obvious row/column alignment issues
- return strict JSON

## Table statuses

```text
keep
discard
needs_correction
corrected
```

The cleaned table output is used for reports and Excel exports.
