"""Create a finance agent that selects between stock and valuation tools."""

from dotenv import load_dotenv
import os
import yfinance as yf
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

groq_model = os.getenv("GROQ_MODEL")
if not groq_model:
    raise RuntimeError("GROQ_MODEL is missing from the environment.")

llm = ChatGroq(model=groq_model)

@tool
def get_stock_price(ticker: str) -> str:
    """Get the current stock price for a given ticker symbol."""
    stock = yf.Ticker(ticker)
    price = stock.info.get("currentPrice")
    return f"The current price of {ticker} is {price} USD"
@tool
def get_market_valuation_of_private_company(company_name: str) -> str:
    """Get the market valuation of a private company."""
    # Static values keep tool selection deterministic for this learning example.
    company_valuations = {
        "OpenAI": "29 billion USD",
        "Stripe": "95 billion USD",
        "SpaceX": "137 billion USD"
    }
    valuation = company_valuations.get(company_name)
    return f"The market valuation of {company_name} is {valuation}" if valuation else f"The market valuation of {company_name} is not publicly available."

# The model chooses a tool from its description and the user's request.
agent = create_agent(
    tools=[get_stock_price, get_market_valuation_of_private_company],
    model=llm,
    system_prompt=(
        "You are the finance agent"
        ),
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "what is the valuation of OpenAI."
                )
            }
        ]
    }
)

print(result["messages"][-1].content)

#python .\agent_lang_chain\2_agent_with_tool\agent_with_tools.py