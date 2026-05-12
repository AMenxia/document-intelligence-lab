from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analysis_runner import (
    ANALYSIS_MODE_OPTIONS,
    DOSSIER_MODE,
    INDIVIDUAL_MODE,
    run_consolidated_dossier,
    run_individual_document_analysis,
    save_blank_analysis_output,
)
from src.config import DEFAULT_LLM_MODEL, DEFAULT_VLM_MODEL, OLLAMA_URL, RUNS_DIR, TEMPLATES_DIR
from src.cropper import update_crop_status, write_selected_manifest
from src.docling_runner import combine_run_outputs, run_docling_for_file
from src.excel_exporter import build_excel_export, extraction_to_excel_tables
from src.file_preview import render_file_preview, render_pdf_path
from src.report_writer import build_report_from_extraction
from src.table_cleanup import run_table_cleanup_for_selected_crops, selected_table_crops
from src.template_loader import blank_structured_extraction, extraction_to_preview_tables, load_templates, template_fields_dataframe
from src.utils import create_run_dir, ensure_dir, read_json, safe_stem, write_json
from src.vlm_runner import run_vlm_for_selected_crops


st.set_page_config(page_title="Document Intelligence Lab", page_icon="📄", layout="wide")

st.title("📄 Document Intelligence Lab")
st.caption("Template-based document analysis with Docling, human crop review, VLM table cleanup, structured JSON, and Excel export.")


# -----------------------------------------------------------------------------
# Load templates
# -----------------------------------------------------------------------------

templates = load_templates(TEMPLATES_DIR)
if not templates:
    st.error("No templates found in the templates/ folder.")
    st.stop()

template_options = list(templates.keys())


# -----------------------------------------------------------------------------
# Sidebar settings
# -----------------------------------------------------------------------------

with st.sidebar:
    st.header("Analysis")

    analysis_mode = st.selectbox(
        "Analysis Mode",
        options=ANALYSIS_MODE_OPTIONS,
        index=0,
        help="Individual mode analyzes each document separately. Dossier mode combines all documents into one consolidated output.",
    )

    st.header("Template")
    selected_template_name = st.selectbox(
        "Template",
        options=template_options,
        format_func=lambda name: templates[name].get("display_name", name),
    )
    selected_template = templates[selected_template_name]

    st.caption(selected_template.get("description", ""))

    st.divider()

    st.header("Models")
    llm_model = st.text_input("LLM", value=DEFAULT_LLM_MODEL)
    vlm_model = st.text_input("VLM", value=DEFAULT_VLM_MODEL)

    st.caption("The VLM model is used for crop summaries and table cleanup.")

    st.divider()

    st.header("Ollama")
    ollama_url = st.text_input("Ollama URL", value=OLLAMA_URL)

    st.divider()

    st.header("Run Folder")
    runs_dir = Path(st.text_input("Runs directory", value=str(RUNS_DIR)))


# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------

defaults = {
    "uploaded_files_data": [],
    "run_result": None,
    "run_dir": None,
    "doc_results": [],
    "excel_tables": None,
    "excel_path": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


tabs = st.tabs(
    [
        "1) Upload + Template",
        "2) Run Docling",
        "3) Crop Review",
        "4) Table Cleanup",
        "5) Analysis + Extraction",
        "6) Excel Preview + Download",
    ]
)


# -----------------------------------------------------------------------------
# Tab 1
# -----------------------------------------------------------------------------

with tabs[0]:
    st.header("1) Upload + Template")

    mode_col, template_col = st.columns(2)
    with mode_col:
        st.subheader("Analysis Mode")
        st.write(f"**{analysis_mode}**")

        if analysis_mode == INDIVIDUAL_MODE:
            st.caption("Each uploaded document is analyzed separately.")
        else:
            st.caption("All uploaded documents are combined into one consolidated dossier.")

    with template_col:
        st.subheader("Selected Template")
        st.write(f"**{selected_template.get('display_name', selected_template_name)}**")
        st.caption(selected_template.get("description", ""))

    field_df = template_fields_dataframe(selected_template)
    st.subheader("Template Fields")
    st.dataframe(field_df, use_container_width=True, hide_index=True)

    st.subheader("Blank structured output preview")
    current_source_names = [item["name"] for item in st.session_state.uploaded_files_data]
    blank = blank_structured_extraction(selected_template, source_files=current_source_names)
    preview_tables = extraction_to_preview_tables(blank)

    preview_tabs = st.tabs(["overview", "documents", "field_values", "people_or_entities", "visual_evidence"])
    for tab, sheet_name in zip(preview_tabs, preview_tables.keys()):
        with tab:
            st.dataframe(preview_tables[sheet_name], use_container_width=True, hide_index=True)

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload one or more documents",
        type=["pdf", "png", "jpg", "jpeg", "webp", "tif", "tiff", "docx", "pptx", "html", "txt", "md"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        st.session_state.uploaded_files_data = [
            {
                "name": uploaded_file.name,
                "type": uploaded_file.type or "application/octet-stream",
                "bytes": uploaded_file.getvalue(),
            }
            for uploaded_file in uploaded_files
        ]

    if not st.session_state.uploaded_files_data:
        st.info("Upload one or more documents to start.")
    else:
        st.subheader("Uploaded files")
        for item in st.session_state.uploaded_files_data:
            with st.expander(item["name"], expanded=len(st.session_state.uploaded_files_data) == 1):
                st.write(f"File type: `{item['type']}`")
                st.write(f"Size: `{len(item['bytes']) / 1024:.1f} KB`")
                render_file_preview(item["type"], item["name"], item["bytes"])


# -----------------------------------------------------------------------------
# Tab 2
# -----------------------------------------------------------------------------

with tabs[1]:
    st.header("2) Run Docling")

    if not st.session_state.uploaded_files_data:
        st.info("Upload files first.")
    else:
        st.write("Current run settings:")
        st.code(f"Analysis Mode: {analysis_mode}\nTemplate: {selected_template_name}")

        if st.button("Run Docling for all files", type="primary", use_container_width=True):
            ensure_dir(runs_dir)
            source_names = [item["name"] for item in st.session_state.uploaded_files_data]
            run_dir = create_run_dir(runs_dir, source_names, selected_template_name)
            input_dir = run_dir / "input"
            output_dir = run_dir / "outputs"

            settings = {
                "analysis_mode": analysis_mode,
                "template_name": selected_template_name,
                "llm_model": llm_model,
                "vlm_model": vlm_model,
                "ollama_url": ollama_url,
                "source_files": source_names,
            }
            write_json(run_dir / "settings.json", settings)
            write_json(output_dir / "selected_template.json", selected_template)

            doc_results = []

            with st.spinner("Running Docling on uploaded files..."):
                for idx, item in enumerate(st.session_state.uploaded_files_data, start=1):
                    doc_id = f"doc_{idx:03d}"
                    suffix = Path(item["name"]).suffix or ".bin"
                    input_path = input_dir / f"{doc_id}_{safe_stem(item['name'])}{suffix}"
                    input_path.write_bytes(item["bytes"])

                    doc_output_dir = output_dir / doc_id
                    result = run_docling_for_file(
                        input_path=input_path,
                        output_dir=doc_output_dir,
                        doc_id=doc_id,
                        original_file_name=item["name"],
                    )
                    doc_results.append(result)

                combined = combine_run_outputs(output_dir, doc_results)

                save_blank_analysis_output(
                    selected_template,
                    doc_results,
                    output_dir,
                    analysis_mode,
                )

            st.session_state.run_dir = str(run_dir)
            st.session_state.doc_results = doc_results
            st.session_state.run_result = {
                "run_dir": str(run_dir),
                "output_dir": str(output_dir),
                "analysis_mode": analysis_mode,
                "settings": settings,
                **combined,
            }
            st.session_state.excel_tables = None
            st.session_state.excel_path = None

            st.success("Docling finished for all files.")

        if st.session_state.run_result:
            result = st.session_state.run_result

            st.subheader("Run outputs")

            summary_rows = []
            for doc_result in st.session_state.doc_results:
                summary_rows.append(
                    {
                        "doc_id": doc_result["doc_id"],
                        "file_name": doc_result["file_name"],
                        "boxes": doc_result["box_count"],
                        "crops": doc_result["crop_count"],
                        "markdown_path": doc_result["markdown_path"],
                        "outlined_pdf_path": doc_result["outlined_pdf_path"],
                    }
                )
            st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

            st.subheader("Individual outlined PDF previews")
            st.caption("Each document gets its own outlined_file.pdf preview.")

            for doc_result in st.session_state.doc_results:
                with st.expander(f"{doc_result['doc_id']} — {doc_result['file_name']}", expanded=True):
                    outlined_path = Path(doc_result["outlined_pdf_path"]) if doc_result.get("outlined_pdf_path") else None
                    markdown_path = Path(doc_result["markdown_path"])
                    json_path = Path(doc_result["json_path"])

                    if outlined_path and outlined_path.exists():
                        st.subheader("outlined_file.pdf")
                        render_pdf_path(outlined_path, height=850)

                        st.download_button(
                            "Download outlined_file.pdf",
                            data=outlined_path.read_bytes(),
                            file_name=f"{doc_result['doc_id']}_outlined_file.pdf",
                            mime="application/pdf",
                            key=f"download_pdf_{doc_result['doc_id']}",
                            use_container_width=True,
                        )
                    else:
                        st.warning("No outlined PDF was created for this document.")

                    col1, col2 = st.columns(2)

                    if markdown_path.exists():
                        col1.download_button(
                            "Download file.md",
                            data=markdown_path.read_bytes(),
                            file_name=f"{doc_result['doc_id']}_file.md",
                            mime="text/markdown",
                            key=f"download_md_{doc_result['doc_id']}",
                            use_container_width=True,
                        )

                    if json_path.exists():
                        col2.download_button(
                            "Download file.json",
                            data=json_path.read_bytes(),
                            file_name=f"{doc_result['doc_id']}_file.json",
                            mime="application/json",
                            key=f"download_json_{doc_result['doc_id']}",
                            use_container_width=True,
                        )

                    with st.expander("Preview Markdown", expanded=False):
                        if markdown_path.exists():
                            st.text_area(
                                "file.md",
                                value=markdown_path.read_text(encoding="utf-8", errors="replace"),
                                height=300,
                                key=f"md_preview_{doc_result['doc_id']}",
                            )


# -----------------------------------------------------------------------------
# Tab 3
# -----------------------------------------------------------------------------

with tabs[2]:
    st.header("3) Crop Review")

    result = st.session_state.run_result
    if not result:
        st.info("Run Docling first.")
    else:
        output_dir = Path(result["output_dir"])
        manifest_path = output_dir / "crop_manifest.json"
        manifest = read_json(manifest_path, fallback=[])

        if not manifest:
            st.info("No crops were generated.")
        else:
            status_filter = st.radio(
                "Filter",
                options=["all", "keep", "discard", "needs_review", "error"],
                horizontal=True,
            )

            visible = manifest if status_filter == "all" else [item for item in manifest if item.get("status") == status_filter]
            st.write(f"Showing `{len(visible)}` of `{len(manifest)}` crops.")

            if st.button("Mark all needs_review crops as keep", use_container_width=True):
                for item in manifest:
                    if item.get("status") == "needs_review":
                        item["status"] = "keep"
                write_json(manifest_path, manifest)
                write_selected_manifest(output_dir, manifest)
                st.success("Updated selected_crop_manifest.json.")
                st.rerun()

            for item in visible:
                crop_path_value = item.get("crop_path")
                with st.container(border=True):
                    col_img, col_meta = st.columns([1, 2])

                    with col_img:
                        if crop_path_value and Path(crop_path_value).exists():
                            st.image(crop_path_value, caption=item.get("crop_id"), use_container_width=True)
                        else:
                            st.warning("Crop image missing.")

                    with col_meta:
                        st.write(f"**{item.get('crop_id')}**")
                        st.write(f"Document: `{item.get('doc_id')}` — `{item.get('file_name')}`")
                        st.write(f"Page: `{item.get('page_no')}`")
                        st.write(f"Type: `{item.get('group')}:{item.get('label')}`")
                        st.write(f"Status: `{item.get('status')}`")
                        if item.get("text_preview"):
                            st.caption(item.get("text_preview"))

                        c1, c2, c3 = st.columns(3)
                        if c1.button("Keep", key=f"keep_{item.get('crop_id')}"):
                            update_crop_status(output_dir, manifest, item.get("crop_id"), "keep")
                            st.rerun()
                        if c2.button("Discard", key=f"discard_{item.get('crop_id')}"):
                            update_crop_status(output_dir, manifest, item.get("crop_id"), "discard")
                            st.rerun()
                        if c3.button("Needs review", key=f"review_{item.get('crop_id')}"):
                            update_crop_status(output_dir, manifest, item.get("crop_id"), "needs_review")
                            st.rerun()

            with st.expander("Preview selected_crop_manifest.json", expanded=False):
                st.json(read_json(output_dir / "selected_crop_manifest.json", fallback=[]))


# -----------------------------------------------------------------------------
# Tab 4
# -----------------------------------------------------------------------------

with tabs[3]:
    st.header("4) Table Cleanup")

    result = st.session_state.run_result
    if not result:
        st.info("Run Docling first.")
    else:
        output_dir = Path(result["output_dir"])
        selected_manifest = read_json(output_dir / "selected_crop_manifest.json", fallback=[])
        table_crops = selected_table_crops(selected_manifest)

        st.write(f"Selected table crops available for cleanup: `{len(table_crops)}`")
        st.caption("This step uses the selected VLM model because table crops are images.")

        if table_crops:
            with st.expander("Preview table crops selected for cleanup", expanded=False):
                for item in table_crops:
                    st.write(f"**{item.get('crop_id')}** — {item.get('file_name')} page {item.get('page_no')}")
                    crop_path = item.get("crop_path")
                    if crop_path and Path(crop_path).exists():
                        st.image(crop_path, use_container_width=True)

        if st.button("Run table cleanup on selected table crops", type="primary", use_container_width=True):
            if not table_crops:
                st.warning("No selected table crops found. Mark table crops as keep or needs_review first.")
            else:
                with st.spinner("Running table cleanup through Ollama..."):
                    cleaned_tables = run_table_cleanup_for_selected_crops(
                        selected_manifest=selected_manifest,
                        output_dir=output_dir,
                        model=vlm_model,
                        ollama_url=ollama_url,
                    )
                st.success(f"Table cleanup finished for {len(cleaned_tables)} table crops.")

        cleaned_tables_path = output_dir / "cleaned_tables.json"
        if cleaned_tables_path.exists():
            cleaned_tables = read_json(cleaned_tables_path, fallback=[])
            st.subheader("cleaned_tables.json")
            st.json(cleaned_tables)

            st.download_button(
                "Download cleaned_tables.json",
                data=cleaned_tables_path.read_bytes(),
                file_name="cleaned_tables.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.info("No cleaned_tables.json yet.")


# -----------------------------------------------------------------------------
# Tab 5
# -----------------------------------------------------------------------------

with tabs[4]:
    st.header("5) Analysis + Extraction")

    result = st.session_state.run_result
    if not result:
        st.info("Run Docling first.")
    else:
        output_dir = Path(result["output_dir"])
        selected_manifest = read_json(output_dir / "selected_crop_manifest.json", fallback=[])

        active_mode = result.get("analysis_mode", analysis_mode)

        st.subheader("Current analysis mode")
        st.write(f"**{active_mode}**")

        st.write(f"Selected crops available for VLM: `{len(selected_manifest)}`")

        if st.button("Run VLM on selected crops", use_container_width=True):
            if not selected_manifest:
                st.warning("No selected crops found.")
            else:
                with st.spinner("Running VLM on selected crops through Ollama..."):
                    vlm_results = run_vlm_for_selected_crops(
                        selected_manifest=selected_manifest,
                        output_dir=output_dir,
                        model=vlm_model,
                        ollama_url=ollama_url,
                    )
                st.success(f"VLM finished for {len(vlm_results)} crops.")

        with st.expander("Preview vlm_results.json", expanded=False):
            st.json(read_json(output_dir / "vlm_results.json", fallback=[]))

        with st.expander("Preview cleaned_tables.json used by extraction", expanded=False):
            st.json(read_json(output_dir / "cleaned_tables.json", fallback=[]))

        st.divider()

        if st.button("Save blank structured output from selected template", use_container_width=True):
            extraction = save_blank_analysis_output(selected_template, st.session_state.doc_results, output_dir, active_mode)
            st.success("Blank structured output saved.")
            st.json(extraction)

        if active_mode == DOSSIER_MODE:
            run_label = "Run Consolidated Dossier"
            run_caption = "Extract each document first, then merge all results into one dossier."
        else:
            run_label = "Run Individual Document Analysis"
            run_caption = "Analyze each uploaded document separately."

        st.caption(run_caption)

        if st.button(run_label, type="primary", use_container_width=True):
            with st.spinner("Running analysis through Ollama..."):
                try:
                    if active_mode == DOSSIER_MODE:
                        extraction = run_consolidated_dossier(
                            template=selected_template,
                            doc_results=st.session_state.doc_results,
                            output_dir=output_dir,
                            model=llm_model,
                            ollama_url=ollama_url,
                        )
                    else:
                        extraction = run_individual_document_analysis(
                            template=selected_template,
                            doc_results=st.session_state.doc_results,
                            output_dir=output_dir,
                            model=llm_model,
                            ollama_url=ollama_url,
                        )
                    report = build_report_from_extraction(output_dir)
                    st.success("Analysis finished.")
                    st.json(extraction)
                    with st.expander("Preview report", expanded=False):
                        st.text_area("report", value=report, height=500)
                except Exception as error:
                    st.error("Analysis failed.")
                    st.exception(error)

        structured_path = output_dir / "structured_extraction.json"
        if structured_path.exists():
            st.subheader("Current structured_extraction.json")
            st.json(read_json(structured_path, fallback={}))

        dossier_path = output_dir / "consolidated_dossier.json"
        if dossier_path.exists():
            st.subheader("Current consolidated_dossier.json")
            st.json(read_json(dossier_path, fallback={}))


# -----------------------------------------------------------------------------
# Tab 6
# -----------------------------------------------------------------------------

with tabs[5]:
    st.header("6) Excel Preview + Download")

    result = st.session_state.run_result
    if not result:
        st.info("Run Docling first.")
    else:
        output_dir = Path(result["output_dir"])
        structured_path = output_dir / "structured_extraction.json"

        if not structured_path.exists():
            st.info("No structured_extraction.json found yet. Save a blank template or run extraction first.")
        else:
            extraction = read_json(structured_path, fallback={})

            st.subheader("Excel sheet preview")
            tables = extraction_to_excel_tables(extraction, output_dir)

            sheet_names = list(tables.keys())
            sheet_tabs = st.tabs(sheet_names)
            for tab, sheet_name in zip(sheet_tabs, sheet_names):
                with tab:
                    st.dataframe(tables[sheet_name], use_container_width=True, hide_index=True)

            if st.button("Generate Excel Export", type="primary", use_container_width=True):
                try:
                    excel_path, tables = build_excel_export(output_dir, extraction)
                    st.session_state.excel_path = str(excel_path)
                    st.session_state.excel_tables = tables
                    st.success(f"Excel export created: {excel_path.name}")
                except Exception as error:
                    st.error("Excel export failed.")
                    st.exception(error)

            excel_path = Path(st.session_state.excel_path) if st.session_state.excel_path else None
            if excel_path and excel_path.exists():
                st.download_button(
                    "Download Excel workbook",
                    data=excel_path.read_bytes(),
                    file_name=excel_path.name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

            report_path = output_dir / "final_report.md"
            if report_path.exists():
                st.download_button(
                    "Download final_report.md",
                    data=report_path.read_bytes(),
                    file_name="final_report.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

            dossier_report_path = output_dir / "consolidated_dossier.md"
            if dossier_report_path.exists():
                st.download_button(
                    "Download consolidated_dossier.md",
                    data=dossier_report_path.read_bytes(),
                    file_name="consolidated_dossier.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
