"""Streamlit UI for the invoice analyzer."""
# python -m streamlit run streamlit_app.py 
import json
from typing import Any

import streamlit as st
from azure.ai.contentunderstanding.models import AnalysisInput
from azure.core.exceptions import AzureError
from streamlit.runtime.uploaded_file_manager import UploadedFile

from analyze import ANALYZER_ID, create_client, to_dictionary


st.set_page_config(page_title="Invoice Analyzer", layout="wide")


def create_uploaded_input(source_file: UploadedFile) -> AnalysisInput:
    """Create an analysis input from a Streamlit upload."""
    return AnalysisInput(
        data=source_file.getvalue(),
        name=source_file.name,
        mime_type=source_file.type or "application/octet-stream",
    )


def run_analysis(input_item: AnalysisInput) -> tuple[Any, dict[str, Any]]:
    """Submit one invoice and return the SDK and JSON-compatible results."""
    credential = None
    try:
        client, credential = create_client()
        analyzed_result = client.begin_analyze(
            analyzer_id=ANALYZER_ID,
            inputs=[input_item],
        ).result()
        return analyzed_result, to_dictionary(analyzed_result)
    finally:
        if credential:
            credential.close()


def render_fields(extracted_fields: dict[str, Any]) -> None:
    """Render extracted values and confidence scores."""
    if not extracted_fields:
        st.info("No invoice fields were returned.")
        return

    for field_name, extracted_field in extracted_fields.items():
        confidence = (
            f" - {extracted_field.confidence:.1%} confidence"
            if extracted_field.confidence is not None
            else ""
        )
        with st.expander(f"{field_name}{confidence}"):
            if isinstance(extracted_field.value, (dict, list)):
                st.json(extracted_field.value)
            else:
                st.write(extracted_field.value)


st.title("Invoice Analyzer")
st.caption("Extract invoice headers, totals, vendor details, and line items with Azure Content Understanding.")

with st.sidebar:
    st.subheader("Analyzer")
    st.code(ANALYZER_ID, language=None)
    st.caption("Credentials are loaded from this sample's .env file or your Azure sign-in.")

source_type = st.segmented_control("Invoice source", ["Upload", "Public URL"], default="Upload")
if source_type == "Upload":
    uploaded_source = st.file_uploader("Choose an invoice", type=["pdf", "png", "jpg", "jpeg", "tif", "tiff"])
    source_input = create_uploaded_input(uploaded_source) if uploaded_source else None
else:
    source_url = st.text_input("Public invoice URL", placeholder="https://example.com/invoice.pdf")
    source_input = AnalysisInput(url=source_url.strip()) if source_url.strip() else None

if st.button("Analyze invoice", type="primary", disabled=source_input is None, use_container_width=True):
    if source_input is None:
        st.stop()
    try:
        with st.spinner("Extracting invoice fields..."):
            result, result_dictionary = run_analysis(source_input)

        if not result.contents:
            st.warning("Analysis completed, but no content was returned.")
        else:
            content = result.contents[0]
            st.success("Analysis complete")
            st.metric("Document category", content.category or "invoice")
            fields_tab, json_tab = st.tabs(["Extracted fields", "Full JSON"])
            with fields_tab:
                render_fields(content.fields or {})
            with json_tab:
                st.json(result_dictionary)

            st.download_button(
                "Download JSON result",
                data=json.dumps(result_dictionary, indent=2, default=str),
                file_name="invoice-result.json",
                mime="application/json",
                use_container_width=True,
            )
    except (AzureError, ValueError, TypeError) as error:
        st.error(f"Analysis failed: {error}")
