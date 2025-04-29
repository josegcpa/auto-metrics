from tqdm import tqdm
from ollama import Client
from pydantic import BaseModel
from .parameters import TEMPERATURE, TOP_P, SEED


def query_model(query: str, data_model: BaseModel, model_str: str):
    client = Client()
    response_stream = client.generate(
        prompt=query,
        model=model_str,
        options={
            "top_p": TOP_P,
            "seed": SEED,
            "temperature": TEMPERATURE,
        },
        format=data_model,
        stream=True,
    )
    response = ""
    for content in tqdm(response_stream):
        response += content["response"]
    return response
