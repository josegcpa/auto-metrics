from google import genai
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from .parameters import TEMPERATURE, TOP_P, SEED


def query_model(query: str, data_model: BaseModel):
    config = GenerateContentConfig(
        temperature=TEMPERATURE,
        top_p=TOP_P,
        seed=SEED,
        response_mime_type="application/json",
        response_schema=data_model,
    )

    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    chat = client.chats.create(model="gemini-2.0-flash-001")

    response = chat.send_message(message=query, config=config)
    response = response.text

    return response
