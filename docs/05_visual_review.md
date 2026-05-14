# Image / Chart VLM Review

## Purpose

Some document content is visual and may not be captured well as plain text.

Examples:

- charts
- diagrams
- figures
- process maps
- screenshots
- product images
- visual summaries

The visual review phase prepares selected visuals for VLM analysis.

## Flow

```text
Docling visual item
↓
crop preview
↓
quick skim result
↓
human review status
↓
optional reviewer note
↓
VLM summary
↓
image_summaries.json
```

## Reviewer notes

Reviewer notes provide optional context before VLM analysis.

Example:

```text
Focus on the product timeline, milestones, and labels.
```

The VLM receives the image crop, nearby context, source metadata, and reviewer note.

## Output

```json
{
  "item_id": "doc_001_item_0042",
  "doc_id": "doc_001",
  "file_name": "example.pdf",
  "page_no": 5,
  "visual_type": "chart",
  "human_note": "Focus on the product timeline.",
  "vlm_summary": "The chart shows a product development timeline...",
  "visible_text": ["Discovery", "Validation", "Launch"],
  "importance": "useful",
  "issues": []
}
```

## Visual statuses

```text
keep
discard
needs_review
```

VLM analysis runs on items marked:

```text
keep
needs_review
```
