from openai import OpenAI
from decouple import config

Client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config("OPENAI_SECRET_KEY"),
)
