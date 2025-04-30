from tqdm import tqdm
from ollama import Client
from pydantic import BaseModel
from .parameters import TEMPERATURE, TOP_P, SEED


def query_model(
    prompt: str, article_text: str, data_model: BaseModel, model_str: str
):
    query = prompt + "\n# Article text\n\n{article}".format(
        article=article_text
    )
    client = Client()
    response_stream = client.chat(
        messages=[
            {"role": "user", "content": query},
        ],
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
        response += content.message.content
    return response
