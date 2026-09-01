from dotenv import load_dotenv
import os
from langchain.messages import HumanMessage
import yfinance as yf
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

groq_model = os.getenv("GROQ_MODEL")
if not groq_model:
    raise RuntimeError("GROQ_MODEL is missing from the environment.")

llm = ChatGroq(model=groq_model,temperature=0)

@tool
def inventory_tool(product_name: str):
    """Check the inventory availability for a given product name."""
    print(f"TOOL CALLED FOR {product_name}")
    inventory = {
        "iPhone 15": "In Stock: Available Items = 2",
        "AirPods Pro": "Out of Stock: Available Items = 0",
        "MacBook Air M3": "In Stock: Available Items = 5",
    }
    return inventory.get(product_name, "Product not found in inventory.")


agent = create_agent(
    tools=[inventory_tool],
    model=llm,
    system_prompt="""
You are an inventory assistant.
- if question is out of scope which is not related to inventory, then just say 
""Sorry, I can only assist with inventory-related questions.""
When a user asks about a product, check the inventory using the inventory tool and provide the availability information.

- Always call the inventory_tool tool with full product name as the argument.
- inventory_tool will return a dictionary which you need to parse to extract stock status and inventory item etc.
- Respond with clear, concise information including:
  1. The stock status (e.g. "In Stock" or "Out of Stock")
  2. The number of available items (e.g. "Available Items = 5")
- if the product is not found in the inventory, respond with "Product not found in inventory."

Never guess or hallucinate information. Do not respond unless the inventory_tool is called.
Keep responses strictly based on the inventory_tool output.
Keep your response short and informative.
"""
)

def run_agent(question:str):
    result = agent.invoke(


        {
            "messages": [
                HumanMessage(content=question)
            ]
        }
    )
    return result["messages"][-1].content

#print(result["messages"][-1].content)



if __name__ == "__main__":
   # question = "Is the iPhone 15 in stock?"
    question = "I want to travel to moon, how much will it cost?"
    answer = run_agent(question)
    print(answer)

#python .\agent_lang_chain\5_func_eval\func_eval.py