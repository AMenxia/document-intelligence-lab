# Architecture

```text
Streamlit UI
  -> Template Loader
  -> Docling Runner
  -> Layout Box Extractor
  -> Cropper
  -> Human Crop Review
  -> Optional VLM Runner
  -> Template Extraction Runner
  -> Excel Exporter
```

The important design choice is that templates control the extraction schema. The output is not just a summary; it is structured JSON plus a formatted Excel workbook.
