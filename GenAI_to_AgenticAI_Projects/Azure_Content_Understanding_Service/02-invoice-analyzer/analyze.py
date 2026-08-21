"""Extract invoice fields with Azure Content Understanding."""

import argparse
import json
import mimetypes
import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.ai.contentunderstanding.models import AnalysisInput, ContentField
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


ANALYZER_ID = "prebuilt-invoice"
ENV_FILE = Path(__file__).with_name(".env")


def create_client() -> tuple[ContentUnderstandingClient, DefaultAzureCredential | None]:
    load_dotenv(ENV_FILE)
    endpoint = os.getenv("CONTENTUNDERSTANDING_ENDPOINT")
    if not endpoint:
        raise ValueError("Set the CONTENTUNDERSTANDING_ENDPOINT environment variable.")

    api_key = os.getenv("CONTENTUNDERSTANDING_KEY")
    if api_key:
        return ContentUnderstandingClient(endpoint, AzureKeyCredential(api_key)), None

    credential = DefaultAzureCredential()
    return ContentUnderstandingClient(endpoint, credential), credential


def print_value(name: str, value: Any, indent: int = 0) -> None:
    prefix = " " * indent
    if isinstance(value, dict):
        print(f"{prefix}{name}:")
        for child_name, child_value in value.items():
            print_value(child_name, child_value, indent + 2)
    elif isinstance(value, list):
        print(f"{prefix}{name}:")
        for index, item in enumerate(value, start=1):
            print_value(f"Item {index}", item, indent + 2)
    else:
        print(f"{prefix}{name}: {value}")


def print_fields(fields: dict[str, ContentField]) -> None:
    for name, field in fields.items():
        confidence = f" ({field.confidence:.1%})" if field.confidence is not None else ""
        print(f"\n{name}{confidence}")
        print_value("Value", field.value, 2)


def to_dictionary(value: Any) -> dict[str, Any]:
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if hasattr(value, "to_dict"):
        return value.to_dict()
    raise TypeError("The SDK result cannot be converted to a dictionary.")


def create_analysis_input(source: str) -> AnalysisInput:
    """Create an SDK input from a public URL or local file path."""
    if urlparse(source).scheme in {"http", "https"}:
        return AnalysisInput(url=source)
    input_path = Path(source)
    if not input_path.is_file():
        raise ValueError(f"Input file does not exist: {input_path}")
    mime_type = mimetypes.guess_type(input_path.name)[0] or "application/octet-stream"
    return AnalysisInput(data=input_path.read_bytes(), name=input_path.name, mime_type=mime_type)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract invoice header and line-item fields.")
    parser.add_argument("input_source", help="Local path or public URL of an invoice PDF or image.")
    parser.add_argument("--output", type=Path, help="Optional path for the full JSON result.")
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()
    credential: DefaultAzureCredential | None = None
    try:
        client, credential = create_client()
        poller = client.begin_analyze(
            analyzer_id=ANALYZER_ID,
            inputs=[create_analysis_input(args.input_source)],
        )
        result = poller.result()
        if not result.contents:
            print("Analysis completed, but no content was returned.")
            return 1

        content = result.contents[0]
        print(f"Category: {content.category or 'invoice'}")
        print_fields(content.fields or {})

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(to_dictionary(result), indent=2, default=str), encoding="utf-8")
            print(f"\nFull result saved to: {args.output}")
        return 0
    except (AzureError, ValueError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    finally:
        if credential:
            credential.close()


if __name__ == "__main__":
    sys.exit(main())