"""Record a named semantic-similarity experiment in LangSmith."""

from langsmith import Client, evaluate, traceable
from langsmith.schemas import Example, Run
from inventory_agent import run_agent
from utils import cosine_similarity
from dotenv import load_dotenv
load_dotenv()

@traceable
def target(inputs: dict) -> dict:
    """Adapt a LangSmith dataset input to the inventory agent contract."""
    question = inputs.get("question", "")
    answer = run_agent(question)
    return {"answer": answer}

client = Client()
dataset_name = "inventorydata"
# Reusing the shared dataset keeps model comparisons consistent.
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

def semantic_match(run: Run, example: Example) -> dict[str, str | float]:
    """Score the generated answer against its reference answer."""
    if example.outputs is None or run.outputs is None:
        raise ValueError("Both reference and run outputs are required for evaluation.")

    expected = example.outputs["answer"]
    actual = run.outputs["answer"]
    sim = cosine_similarity(expected, actual)
    return {
        "key": "semantic_match",
        "score": float(sim)
    }

# The prefix groups this candidate model's run in the LangSmith UI.
evaluate(
    target,
    client=client,
    data=dataset_name,
    evaluators=[semantic_match],
    experiment_prefix="run with openai"
) # type: ignore

# python .\agent_lang_chain\7_eval_op_metrics\func_eval.py