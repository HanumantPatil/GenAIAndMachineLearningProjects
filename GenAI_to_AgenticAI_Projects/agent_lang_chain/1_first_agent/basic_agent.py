"""Create a news agent with SerpAPI search and a Google News RSS fallback."""

from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from urllib.request import urlopen
from xml.etree import ElementTree

load_dotenv()

from langchain.agents import create_agent
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import tool
from langchain_groq import ChatGroq

serpapi_key = os.getenv("SERPAPI_API_KEY")
groq_model = os.getenv("GROQ_MODEL")
if not groq_model:
    raise RuntimeError("GROQ_MODEL is missing from the environment.")

llm = ChatGroq(model=groq_model)

# Restrict the primary search provider to recent news results.
serp = SerpAPIWrapper(
    serpapi_api_key = serpapi_key,
    params={
        "tbm": "nws", # Search news
        "tbs": "qdr:d" # Search news from the past day
    }
)


def search_google_news_rss(query: str) -> str:
    """Search Google News RSS without requiring an API key."""
    encoded_query = quote_plus(f"{query} when:1d")
    url = (
        "https://news.google.com/rss/search"
        f"?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    )

    with urlopen(url, timeout=15) as response:  # noqa: S310
        root = ElementTree.fromstring(response.read())

    articles = []
    for item in root.findall("./channel/item")[:5]:
        title = item.findtext("title", default="Unknown title")
        link = item.findtext("link", default="")
        published = item.findtext("pubDate", default="Unknown date")
        articles.append(f"Title: {title}\nDate: {published}\nURL: {link}")

    return "\n\n".join(articles) or "No recent news articles were found."

@tool
def search_news(query: str) -> str:
    """Search for recent news articles and return titles, dates, and URLs."""
    try:
        return serp.run(query)
    except ValueError as error:
        if "Invalid API key" not in str(error):
            raise
        # Keep the example usable when SerpAPI rejects the configured key.
        return search_google_news_rss(query)

agent = create_agent(
    tools=[search_news],
    model=llm,
    system_prompt=(
        "You are a news reporter who reports news using a simple language."
        "in 3 lines along with date of news"
        "give top 3 news articles"
        ),
)

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Tell me the most latest breaking political news from the india"
                    "along with the web url of news articles"
                )
            }
        ]
    }
)

print(result["messages"][-1].content)

#python .\agent_lang_chain\1_first_agent\basic_agent.py