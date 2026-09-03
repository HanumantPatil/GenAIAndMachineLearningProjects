import json

from langsmith import Client, evaluate, traceable
from langsmith.schemas import Example, Run
from inventory_agent import run_agent
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

LLM_AS_JUDGE_MODEL_NAME = "openai/gpt-oss-120b"
judge = ChatGroq(model=LLM_AS_JUDGE_MODEL_NAME, temperature=0) # type: ignore

@traceable
def target(inputs: dict) -> dict:
    question = inputs.get("question", "")
    answer = run_agent(question)
    return {"answer": answer}

client = Client()
dataset_name = "inventorydata"
if not client.has_dataset(dataset_name= dataset_name):
    client.create_dataset(dataset_name)
    client.create_examples(
            dataset_name=dataset_name,
            examples=[
                {
                    "inputs": {"question": "What is the stock status of iPhone 15?"},
                    "outputs": {"answer": "The iPhone 15 is currently in stock with 2 units available."},
                },
                {
                    "inputs": {"question": "Is AirPods Pro available?"},
                    "outputs": {"answer": "The AirPods Pro is currently out of stock. There are 0 available items."},
                },
                {
                    "inputs": {"question": "How many iPhone 15 units are available?"},
                    "outputs": {"answer": "The iPhone 15 is currently in stock with 2 units available."},
                },
                {
                    "inputs": {"question": "Do you have Samsung Galaxy S23?"},
                    "outputs": {"answer": "The product is not available in our inventory"},
                },
                {
                    "inputs": {"question": "Can you tell me the recipe of Vada Pav?"},
                    "outputs": {"answer": "Sorry, I can’t assist with that"},
                }
            ],
        )

JUDGE_PROMPT = """You are a helpful and precise assistant for checking the correctness of the answer.
Question: {question}
Expected Answer: {expected}
Actual Answer: {actual}
Please compare the actual answer with the expected answer and given a score between 0 and 1 base on the correctness of the answer.
return only valid json like:
{{"score": <number>}}
"""

def llm_as_judge(run: Run, example: Example) -> dict[str, str | float]:
    if example.inputs is None or example.outputs is None or run.outputs is None:
        raise ValueError("Example inputs, reference outputs, and run outputs are required for evaluation.")

    question = example.inputs["question"]
    expected = example.outputs["answer"]
    actual = run.outputs["answer"]
    msg = JUDGE_PROMPT.format(question=question, expected=expected, actual=actual)
    
    res = judge.invoke(msg)

    if not isinstance(res.content, str):
        raise TypeError("The judge response must contain JSON text.")

    data = json.loads(res.content)
    score = float(data["score"])
    return {
        "key": "llm_as_judge",
        "score": float(score)
    }

evaluate(
    target,
    client=client,
    data=dataset_name,
    evaluators=[llm_as_judge]    
) # type: ignore

# python .\agent_lang_chain\6_eval_llm_judge.py\func_eval.py