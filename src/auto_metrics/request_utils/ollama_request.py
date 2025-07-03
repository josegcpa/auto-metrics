"""
Functions to query a model for a given prompt and article text using Ollama.
"""

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
    parameters: Parameters = Parameters(),
):
    """
    Query a model for a given prompt and article text.

    Args:
        prompt (str): The prompt to query the model with.
        article_text (str): The article text to query the model with.
        data_model (BaseModel): The data model to use for the query.
        model_str (str): The model to use for the query.
        max_tokens (int | None): The maximum number of tokens to generate.
        parameters (Parameters): The parameters to use for the query.

    Returns:
        str: The response from the model.
    """
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
            "top_p": parameters.TOP_P,
            "top_k": parameters.TOP_K,
            "seed": parameters.SEED,
            "frequency_penalty": parameters.FREQUENCY_PENALTY,
            "presence_penalty": parameters.PRESENCE_PENALTY,
            "temperature": parameters.TEMPERATURE,
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
