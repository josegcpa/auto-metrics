import os
from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from .parameters import TEMPERATURE, TOP_P, SEED


def query_model(prompt: str, article_text: str, data_model: BaseModel):
    query = prompt + "\n# Article text\n\n{article}".format(
        article=article_text
    )
    config = GenerateContentConfig(
        temperature=TEMPERATURE,
        top_p=TOP_P,
        seed=SEED,
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
