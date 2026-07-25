
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


import os

api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7, api_key=api_key)

def extract(paragraph):
    # Placeholder for the actual extraction logic


    prompt = '''
    From the below news article, extract revenue and eps in JSON format containing the
    following keys: 'revenue_actual', 'revenue_expected', 'eps_actual', 'eps_expected'. 

    Each value should have a unit such as million or billion.

    Only return the valid JSON. No preamble.

    Article
    =======
    {article}

    '''
    pt = PromptTemplate.from_template(prompt)

    chain =  pt | llm 

    chain_output = chain.invoke({"article": paragraph})
    # This function should return a dictionary with keys: 'revenue_expected', 'revenue_actual', 'eps_expected', 'eps_actual'

    parser = JsonOutputParser()
    output_json = parser.parse(chain_output.content)
    return {
        'revenue_expected': output_json.get('revenue_expected', 1000000),
        'revenue_actual': output_json.get('revenue_actual', 950000),
        'eps_expected': output_json.get('eps_expected', 2.5),
        'eps_actual': output_json.get('eps_actual', 2.3)
    }