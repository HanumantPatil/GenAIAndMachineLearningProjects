"""Streamlit UI for the call-center analyzer."""
# python -m streamlit run streamlit_app.py 
import json
from typing import Any

import streamlit as st
from azure.ai.contentunderstanding.models import AnalysisInput
from azure.core.exceptions import AzureError
from streamlit.runtime.uploaded_file_manager import UploadedFile

from analyze import ANALYZER_ID, create_client, to_dictionary


st.set_page_config(page_title="Call Center Analyzer", layout="wide")


def create_uploaded_input(source_file: UploadedFile) -> AnalysisInput:
    """Create an analysis input from a Streamlit upload."""
    return AnalysisInput(
        data=source_file.getvalue(),
        name=source_file.name,
        mime_type=source_file.type or "application/octet-stream",
    )


def run_analysis(input_item: AnalysisInput) -> tuple[Any, dict[str, Any]]:
    """Submit one recording and return the SDK and JSON-compatible results."""
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


def render_insights(extracted_fields: dict[str, Any]) -> None:
    """Render call insights and confidence scores."""
    if not extracted_fields:
        st.info("No call insights were returned.")
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


st.title("Call Center Analyzer")
st.caption("Transcribe recordings and review call insights with Azure Content Understanding.")

with st.sidebar:
    st.subheader("Analyzer")
    st.code(ANALYZER_ID, language=None)
    st.caption("Credentials are loaded from this sample's .env file or your Azure sign-in.")

source_type = st.segmented_control("Recording source", ["Upload", "Public URL"], default="Upload")
if source_type == "Upload":
    uploaded_source = st.file_uploader(
        "Choose an audio or video recording",
        type=["mp3", "wav", "m4a", "mp4", "mov", "webm"],
    )
    source_input = create_uploaded_input(uploaded_source) if uploaded_source else None
else:
    source_url = st.text_input("Public recording URL", placeholder="https://example.com/call.mp3")
    source_input = AnalysisInput(url=source_url.strip()) if source_url.strip() else None

if st.button("Analyze recording", type="primary", disabled=source_input is None, use_container_width=True):
    if source_input is None:
        st.stop()
    try:
        with st.spinner("Transcribing and analyzing the recording..."):
            result, result_dictionary = run_analysis(source_input)

        if not result.contents:
            st.warning("Analysis completed, but no content was returned.")
        else:
            content = result.contents[0]
            st.success("Analysis complete")
            transcript_tab, insights_tab, json_tab = st.tabs(["Transcript", "Call insights", "Full JSON"])
            with transcript_tab:
                st.markdown(content.markdown or "No transcript was returned.")
            with insights_tab:
                render_insights(content.fields or {})
            with json_tab:
                st.json(result_dictionary)

            st.download_button(
                "Download JSON result",
                data=json.dumps(result_dictionary, indent=2, default=str),
                file_name="call-center-result.json",
                mime="application/json",
                use_container_width=True,
            )
    except (AzureError, ValueError, TypeError) as error:
        st.error(f"Analysis failed: {error}")
