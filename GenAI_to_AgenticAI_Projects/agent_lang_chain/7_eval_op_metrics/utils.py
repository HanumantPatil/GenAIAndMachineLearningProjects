from dotenv import load_dotenv
import os
import numpy as np
from torchgen import model
load_dotenv()

## genrate cosin similarity using sentence transformer 
from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer('all-MiniLM-L6-v2')

def cosine_similarity(sentence1: str, sentence2: str) -> float:
    embedding1 = _model.encode(sentence1, convert_to_tensor=True)
    embedding2 = _model.encode(sentence2, convert_to_tensor=True)
    similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    return float(np.clip(similarity, 0.0, 1.0))


if __name__ == "__main__":
    pairs = [
        ("I love programming.", "I enjoy coding."),
        ("The sky is blue.", "The ocean is vast."),
        ("Apples are red.", "Bananas are yellow."),
        ("The cat sta on the mat.", "A Feline rested on the rug.")
    ]
    for sentence1, sentence2 in pairs:
        similarity = cosine_similarity(sentence1, sentence2)
        print(f"Cosine similarity between '{sentence1}' and '{sentence2}': {similarity}")

# python agent_lang_chain/5_func_eval/utils.py