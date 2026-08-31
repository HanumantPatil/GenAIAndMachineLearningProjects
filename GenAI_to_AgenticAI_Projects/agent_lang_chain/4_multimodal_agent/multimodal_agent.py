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

llm = ChatGroq(model=groq_model,temperature=0)


agent = create_agent(
    tools=[],
    model=llm,
    system_prompt="""
You are an image agent
"""
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "which animal is in this image?print only the name of the animal.https://wildlifeillinois.org/wp-content/uploads/2019/02/Chipmunk-Gonthier.jpeg"
                )
            }
        ]
    }
)

print(result["messages"][-1].content)

#python .\agent_lang_chain\4_multimodal_agent\multimodal_agent.py