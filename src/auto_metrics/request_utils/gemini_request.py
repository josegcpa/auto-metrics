"""
Functions to query a model for a given prompt and article text using Google 
Gemini.
"""

import os
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from .parameters import Parameters


def query_model(
    prompt: str,
    article_text: str,
    data_model: BaseModel,
    parameters: Parameters = Parameters(),
) -> str:
    """
    Query a model for a given prompt and article text.

    Args:
        prompt (str): The prompt to query the model with.
        article_text (str): The article text to query the model with.
        data_model (BaseModel): The data model to use for the query.
        parameters (Parameters): The parameters to use for the query.

    Returns:
        str: The response from the model.
    """
    query = prompt + "\n# Article text\n\n{article}".format(
        article=article_text
    )
    config = GenerateContentConfig(
        temperature=parameters.TEMPERATURE,
        top_p=parameters.TOP_P,
        top_k=parameters.TOP_K,
        seed=parameters.SEED,
        frequency_penalty=parameters.FREQUENCY_PENALTY,
        presence_penalty=parameters.PRESENCE_PENALTY,
        response_mime_type="application/json",
        response_schema=data_model,
    )

    if "GOOGLE_API_KEY" not in os.environ:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.chats.create(model="gemini-2.0-flash-001")

    response = chat.send_message(message=query, config=config)
    response = response.text

    return response
