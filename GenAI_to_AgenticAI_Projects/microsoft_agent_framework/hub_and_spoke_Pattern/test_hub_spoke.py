"""Offline tests for specialist delegation and the real framework tool loop."""

import asyncio
from collections.abc import Iterator, Mapping, Sequence

import pytest
from agent_framework import ChatResponse, Content, FunctionTool, Message, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from hub_spoke import ResearchSpokes, main, run_research


@pytest.fixture
def client() -> Iterator[FoundryChatClient]:
    with DefaultAzureCredential() as credential:
        yield FoundryChatClient(
            project_endpoint="https://example.services.ai.azure.com/api/projects/test",
            model="test-model",
            credential=credential,
        )


def text_response(text: str) -> ChatResponse:
    return ChatResponse(messages=[Message("assistant", [text])])


def tool_response(name: str, arguments: Mapping[str, object]) -> ChatResponse:
    return ChatResponse(
        messages=[
            Message(
                "assistant",
                [Content.from_function_call(name, name, arguments=arguments)],
            )
        ]
    )


def script_responses(
    monkeypatch: pytest.MonkeyPatch, responses: list[ChatResponse]
) -> list[list[Message]]:
    calls: list[list[Message]] = []
    pending = iter(responses)

    async def respond(
        self: FoundryChatClient,
        *,
        messages: Sequence[Message],
        options: Mapping[str, object],
        stream: bool = False,
        **kwargs: object,
    ) -> ChatResponse:
        calls.append(list(messages))
        return next(pending)

    monkeypatch.setattr(FoundryChatClient, "_inner_get_response", respond)
    return calls


def test_given_tool_calls_when_hub_runs_then_spokes_return_results_to_hub(
    client: FoundryChatClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    calls = script_responses(
        monkeypatch,
        [
            tool_response(
                "invoke_market_analysis_agent", {"asset_classes": ["equities", "bonds"]}
            ),
            text_response("Market report: interest rates affect both asset classes."),
            tool_response("invoke_risk_assessment_agent", {}),
            text_response("Risk report: equity volatility and bond duration risk."),
            text_response("Combined educational summary."),
        ],
    )

    # Act
    result = asyncio.run(run_research(client, "Compare equities and bonds."))

    # Assert
    assert result == "Combined educational summary."
    assert len(calls) == 5
    assert "equities, bonds" in calls[1][-1].text
    assert "Market report:" in calls[3][-1].text
    results = [
        content
        for message in calls[4]
        for content in message.contents
        if content.type == "function_result"
    ]
    assert len(results) == 2
    assert "Market report:" in str(results[0].result)
    assert "Risk report:" in str(results[1].result)


def test_given_no_market_report_when_risk_runs_then_rejects_call(
    client: FoundryChatClient,
) -> None:
    # Arrange
    spokes = ResearchSpokes(client)

    # Act & Assert
    with pytest.raises(ValueError, match="market analysis before"):
        asyncio.run(spokes.invoke_risk_assessment_agent())


def test_given_market_tool_when_schema_generated_then_requires_string_array(
    client: FoundryChatClient,
) -> None:
    # Arrange
    spokes = ResearchSpokes(client)

    # Act
    market_tool = tool(spokes.invoke_market_analysis_agent)

    # Assert
    assert isinstance(market_tool, FunctionTool)
    schema = market_tool.parameters()
    assert schema["required"] == ["asset_classes"]
    assert schema["properties"]["asset_classes"]["type"] == "array"
    assert schema["properties"]["asset_classes"]["items"]["type"] == "string"


def test_given_separate_requests_when_spokes_created_then_reports_are_isolated(
    client: FoundryChatClient,
) -> None:
    # Arrange
    first = ResearchSpokes(client)
    first.market_report = "First request's report."

    # Act
    second = ResearchSpokes(client)

    # Assert
    assert second.market_report is None
    assert second.risk_report is None


@pytest.mark.parametrize("asset_classes", [[], [""], ["bonds", "  "]])
def test_given_invalid_assets_when_market_runs_then_rejects_call(
    client: FoundryChatClient, asset_classes: list[str]
) -> None:
    # Arrange
    spokes = ResearchSpokes(client)

    # Act & Assert
    with pytest.raises(ValueError, match="nonblank asset"):
        asyncio.run(spokes.invoke_market_analysis_agent(asset_classes))


def test_given_previous_reports_when_market_runs_then_invalidates_old_risk(
    client: FoundryChatClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    spokes = ResearchSpokes(client)
    spokes.market_report = "Old market report."
    spokes.risk_report = "Old risk report."
    script_responses(monkeypatch, [text_response("New market report.")])

    # Act
    result = asyncio.run(spokes.invoke_market_analysis_agent(["real estate"]))

    # Assert
    assert result == spokes.market_report == "New market report."
    assert spokes.risk_report is None


@pytest.mark.parametrize("spoke", ["market", "risk"])
def test_given_empty_spoke_response_when_called_then_raises(
    client: FoundryChatClient, monkeypatch: pytest.MonkeyPatch, spoke: str
) -> None:
    # Arrange
    spokes = ResearchSpokes(client)
    script_responses(monkeypatch, [text_response("   ")])

    # Act & Assert
    with pytest.raises(RuntimeError, match="empty report"):
        if spoke == "market":
            asyncio.run(spokes.invoke_market_analysis_agent(["bonds"]))
        else:
            spokes.market_report = "Market report."
            asyncio.run(spokes.invoke_risk_assessment_agent())


def test_given_hub_skips_spokes_when_run_then_rejects_summary(
    client: FoundryChatClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    script_responses(monkeypatch, [text_response("Unsupported summary.")])

    # Act & Assert
    with pytest.raises(RuntimeError, match="both specialist assessments"):
        asyncio.run(run_research(client, "Compare bonds and equities."))


def test_given_empty_hub_summary_when_spokes_complete_then_raises(
    client: FoundryChatClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    script_responses(
        monkeypatch,
        [
            tool_response("invoke_market_analysis_agent", {"asset_classes": ["bonds"]}),
            text_response("Market report."),
            tool_response("invoke_risk_assessment_agent", {}),
            text_response("Risk report."),
            text_response(""),
        ],
    )

    # Act & Assert
    with pytest.raises(RuntimeError, match="empty research summary"):
        asyncio.run(run_research(client, "Analyze bonds."))


def test_given_blank_request_when_run_then_rejects_request(
    client: FoundryChatClient,
) -> None:
    # Act & Assert
    with pytest.raises(ValueError, match="must not be blank"):
        asyncio.run(run_research(client, "  "))


def test_given_missing_configuration_when_main_runs_then_returns_configuration_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr("hub_spoke.load_dotenv", lambda: None)
    monkeypatch.delenv("AZURE_AI_PROJECT_ENDPOINT", raising=False)
    monkeypatch.delenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", raising=False)

    # Act
    result = asyncio.run(main())

    # Assert
    assert result == 2
