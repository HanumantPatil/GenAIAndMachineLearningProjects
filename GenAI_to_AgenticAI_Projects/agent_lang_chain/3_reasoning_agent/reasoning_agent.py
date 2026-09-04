"""Demonstrate prompt-guided numerical reasoning without external tools."""

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


# An empty tool list isolates the model's own reasoning behavior.
agent = create_agent(
    tools=[],
    model=llm,
    system_prompt="""
You are an advanced reasoning assistant.
list all the steps you carry to reason with numbers.
if you are using formula, it should not be in Latex but in plain formulas.
"""
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "how much time it take a cheetah to run from New Delhi to Mumbai?"
                )
            }
        ]
    }
)

print(result["messages"][-1].content)

#python .\agent_lang_chain\3_reasoning_agent\reasoning_agent.py