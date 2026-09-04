"""Classify local clothing images with structured multimodal message content."""

import base64
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

groq_vision_model = os.getenv("GROQ_VISION_MODEL", "qwen/qwen3.8-27b")
llm = ChatGroq(model=groq_vision_model, temperature=0, max_tokens=1000)

def encode_image_to_base64(image_path: str) -> str:
    """Encode a JPEG as a data URL accepted by multimodal chat models."""
    with open(image_path, "rb") as image_file:
        return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

# Resolve assets from the script location so the launch directory does not matter.
base_dir = Path(__file__).parent
image_url_01 = encode_image_to_base64(str(base_dir / "images/image1.jpg"))
image_url_02 = encode_image_to_base64(str(base_dir / "images/image2.jpg"))
image_url_03 = encode_image_to_base64(str(base_dir / "images/image3.jpg"))

# LangChain accepts text and image URL blocks in one human message.
human_content = [
    {
        "type": "text","text": "Analyze each image and return a json array of records as instance."
    },
    {
        "type": "image_url", "image_url": {"url": image_url_01}
    },
    {
        "type": "image_url", "image_url": {"url": image_url_02}
    },
    {
        "type": "image_url", "image_url": {"url": image_url_03}
    }
]

SYSTEM_PROMPT = """
For each image, generate a json record that looks like this:
{
    "item_name":"sari",
    "item_code":"ITM001",
    "color":"red",
    "gender":"female",
    "age_category":"adult"
}
output must be json string that python parse it directly.
do not put any pre-amble instructions or event 'json' in front of the response string.
item_name should be one of the following: "sari", "t-shirt", "jeans", "dress", "jacket".
Use these item codes: sari=ITM001, t-shirt=ITM002, jeans=ITM003, jacket=ITM004, dress=ITM005.
age_category should be one of the following: "child", "teen", "adult", "senior".
"""
agent = create_agent(
    tools=[],
    model=llm,
    system_prompt=SYSTEM_PROMPT
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": human_content
            }
        ]
    }
)

print(result["messages"][-1].content)

#python .\agent_lang_chain\4_multimodal_agent\multimodal_agent_classify.py