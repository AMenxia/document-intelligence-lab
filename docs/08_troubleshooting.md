# Troubleshooting

## Crop preview shows the wrong location

This usually points to a bounding box coordinate conversion issue.

Check:

- page number
- bbox values
- coordinate origin
- page width/height
- crop preview
- outlined PDF

If raw table content is correct but the crop is wrong, the table extraction is probably working and the visual crop math needs adjustment.

## Outlined PDF boxes are shifted

The outlined PDF and crop generation should use the same coordinate conversion logic.

If both are shifted in the same way, debug bbox conversion.

## Table correction returns invalid JSON

Try:

- lower model temperature
- stricter JSON-only prompt
- one retry pass
- code-fence stripping before JSON parsing
- saving failed model output for inspection

## Table correction changes facts

The correction prompt should require the model to preserve:

- numbers
- dates
- names
- labels
- units
- source wording when possible

The raw table output should remain available for comparison.

## VLM summaries are too generic

Add a reviewer note that tells the VLM what to focus on.

Example:

```text
Focus on the axis labels, trend direction, and milestone dates.
```

## Embedded PDF preview is blank

Some browsers do not render embedded PDFs consistently.

Use one of these alternatives:

- open the PDF directly
- download the PDF
- render PDF pages as images
- view the outlined PDF output

## Ollama model is not responding

Check that Ollama is running:

```bash
ollama serve
```

Check installed models:

```bash
ollama list
```

Confirm the app is using the correct local URL:

```text
http://localhost:11434
```

## Outputs look stale

Delete the previous run folder and rerun the pipeline after code changes.
