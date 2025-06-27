from tqdm import tqdm
from ollama import Client
from pydantic import BaseModel
from auto_metrics.request_utils.parameters import Parameters


def query_model(
    prompt: str,
    article_text: str,
    data_model: BaseModel,
    model_str: str,
    max_tokens: int | None = None,
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
            "top_p": Parameters.TOP_P,
            "top_k": Parameters.TOP_K,
            "seed": Parameters.SEED,
            "frequency_penalty": Parameters.FREQUENCY_PENALTY,
            "presence_penalty": Parameters.PRESENCE_PENALTY,
            "temperature": Parameters.TEMPERATURE,
        },
        format=data_model,
        stream=True,
    )
    response = ""
    for i, content in tqdm(enumerate(response_stream)):
        response += content.message.content
        if max_tokens is not None:
            if i > max_tokens:
                break
    return response
