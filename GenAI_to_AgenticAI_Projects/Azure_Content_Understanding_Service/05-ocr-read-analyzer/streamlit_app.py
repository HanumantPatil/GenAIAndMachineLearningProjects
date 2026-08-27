"""Streamlit UI for the OCR read analyzer."""
# python -m streamlit run streamlit_app.py 
import json
from typing import Any

import streamlit as st
from azure.ai.contentunderstanding.models import AnalysisInput
from azure.core.exceptions import AzureError
from streamlit.runtime.uploaded_file_manager import UploadedFile

from analyze import ANALYZER_ID, create_client, to_dictionary


st.set_page_config(page_title="OCR Read Analyzer", layout="wide")


def create_uploaded_input(source_file: UploadedFile) -> AnalysisInput:
    """Create an analysis input from a Streamlit upload."""
    return AnalysisInput(
        data=source_file.getvalue(),
        name=source_file.name,
        mime_type=source_file.type or "application/octet-stream",
    )


def run_analysis(input_item: AnalysisInput) -> tuple[Any, dict[str, Any]]:
    """Submit one document and return the SDK and JSON-compatible results."""
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


st.title("OCR Read Analyzer")
st.caption("Recognize printed and handwritten text with Azure Content Understanding.")

with st.sidebar:
    st.subheader("Analyzer")
    st.code(ANALYZER_ID, language=None)
    st.caption("Credentials are loaded from this sample's .env file or your Azure sign-in.")

source_type = st.segmented_control("Document source", ["Upload", "Public URL"], default="Upload")
if source_type == "Upload":
    uploaded_source = st.file_uploader("Choose a PDF or image", type=["pdf", "png", "jpg", "jpeg", "tif", "tiff"])
    source_input = create_uploaded_input(uploaded_source) if uploaded_source else None
else:
    source_url = st.text_input("Public document URL", placeholder="https://example.com/document.png")
    source_input = AnalysisInput(url=source_url.strip()) if source_url.strip() else None

if st.button("Read document", type="primary", disabled=source_input is None, use_container_width=True):
    if source_input is None:
        st.stop()
    try:
        with st.spinner("Recognizing text..."):
            result, result_dictionary = run_analysis(source_input)

        if not result.contents:
            st.warning("Analysis completed, but no content was returned.")
        else:
            st.success("Analysis complete")
            text_tab, json_tab = st.tabs(["Recognized text", "Full JSON"])
            with text_tab:
                st.markdown(result.contents[0].markdown or "No text was returned.")
            with json_tab:
                st.json(result_dictionary)

            st.download_button(
                "Download JSON result",
                data=json.dumps(result_dictionary, indent=2, default=str),
                file_name="ocr-read-result.json",
                mime="application/json",
                use_container_width=True,
            )
    except (AzureError, ValueError, TypeError) as error:
        st.error(f"Analysis failed: {error}")
