from agent_framework import Agent, AgentResponseUpdate
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import HandoffBuilder
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    credential = DefaultAzureCredential()

    chat_client = FoundryChatClient(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
        credential=credential,
    )
    # Agent instructions focus on OUTPUT, not on compressing context for the next agent
    credit_analyst = Agent(
        client=chat_client,
        name="credit_analyst",
        require_per_service_call_history_persistence=True,
        instructions="""You analyze debt structure and credit metrics.
    Complete your analysis and return a structured JSON result with:
    - debt_to_equity_ratio
    - interest_coverage_ratio
    - maturity_profile (list of {year, amount_millions})
    - credit_assessment (string: STRONG / ADEQUATE / STRESSED)

    When you encounter convertible securities, hand off to equity_valuation_specialist.
        Don't summarize prior analysis—return your findings in full structured form.""",
    )
    equity_specialist = Agent(
        client=chat_client,
        name="equity_valuation_specialist",
        require_per_service_call_history_persistence=True,
        instructions="""You value equity-linked instruments including convertible securities.
    The full conversation history (including the credit analyst's findings) is available to you.
    Build on the prior credit analysis—don't re-analyze what has already been done.
    Return valuation results as JSON with: instrument_type, fair_value_estimate, dilution_impact.""",
    )

    workflow = (
        HandoffBuilder(
            name="credit_equity_handoff",
            participants=[credit_analyst, equity_specialist],
        )
        .with_start_agent(credit_analyst)
        .add_handoff(credit_analyst, [equity_specialist])
        .with_autonomous_mode()
        .build()
    )

    MAX_HANDOFF_DEPTH = 4
    chain_depth = 0
    final_results = []
    # add research_query for testing purposes, put sample data here
    research_query = (
        "Analyze this fictional company's credit metrics and convertible securities. "
        "All amounts are in USD millions unless stated otherwise: total debt 500, "
        "total equity 1000, EBIT 120, annual interest expense 30. "
        "Debt maturities: 2027: 100, 2028: 150, 2030: 250. "
        "The 2030 debt is convertible with a 4% annual coupon, a conversion price "
        "of USD 50 per share, and a current share price of USD 45. "
        "There are 100 million shares outstanding. State any additional valuation assumptions."
    )
    async for event in workflow.run(research_query, stream=True):
        if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
            final_results.append({
                "agent": event.data.author_name,
                "content": event.data.text,
            })
            print(event.data.text, end="", flush=True)
        elif event.type == "handoff_sent":
            chain_depth += 1
            if chain_depth >= MAX_HANDOFF_DEPTH:
                print(f"\nChain depth limit reached after {chain_depth} handoffs.")
                break
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

# python .\microsoft_agent_framework\handoff_reliability\handoff.py