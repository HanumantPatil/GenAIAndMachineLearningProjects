"""Demonstrate masking and redaction of PII returned by an agent tool."""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

LLM_AS_JUDGE_MODEL_NAME = "openai/gpt-oss-120b"
llm = ChatGroq(model=LLM_AS_JUDGE_MODEL_NAME, temperature=0)  # type: ignore


@tool
def get_customer_info_tool(customer_name: str):
    """Retrieve customer information based on the customer name."""
    # Use test records so the middleware behavior is deterministic.
    customer_info = {
        "Krishna": {
            "email": "ktishna_001@abc.com",
            "credit_card": "4111-1111-1111-1111",
            "name": "Krishna",
            "loyalty_status": "Gold",
        },
        "Alice": {
            "email": "alice_001@abc.com",
            "credit_card": "4111-1111-1111-1112",
            "name": "Alice",
            "loyalty_status": "Silver",
        },
        "Bob": {
            "email": "bob_001@abc.com",
            "credit_card": "4111-1111-1111-1113",
            "name": "Bob",
            "loyalty_status": "Platinum",
        },
    }
    return customer_info.get(customer_name, "Customer not found")


agent = create_agent(
    system_prompt="""You are a customer service assistant.
    You have access to the get_customer_info_tool which provides customer information based on the customer name.
    When a user asks for information about a customer, use the get_customer_info_tool to retrieve the relevant details.
""",
    model=llm,
    tools=[get_customer_info_tool],
    middleware=[
        # The built-in card detector masks only values that pass the Luhn check.
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_tool_results=True,
        ),
        # Scan both the tool response and the model's final response for email.
        PIIMiddleware(
            "email", strategy="redact", apply_to_tool_results=True, apply_to_output=True
        ),
    ],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Get information for customer Krishna"}]}
)

print(result["messages"][-1].content)

# python .\agent_lang_chain\8_guardrails\guardrails_1.py
