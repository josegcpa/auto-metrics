import os
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from .parameters import Parameters


def query_model(prompt: str, article_text: str, data_model: BaseModel):
    query = prompt + "\n# Article text\n\n{article}".format(
        article=article_text
    )
    config = GenerateContentConfig(
        temperature=Parameters.TEMPERATURE,
        top_p=Parameters.TOP_P,
        top_k=Parameters.TOP_K,
        seed=Parameters.SEED,
        frequency_penalty=Parameters.FREQUENCY_PENALTY,
        presence_penalty=Parameters.PRESENCE_PENALTY,
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
