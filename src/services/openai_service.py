

from openai.types.chat import ChatCompletion
from src.data.config import settings
from src.utils.loader import openai_client

class OpenAIService:
    openai_client = openai_client

    @classmethod
    async def get_gpt_response(cls, messages: str) -> str:
        # print(messages)
        response = await cls.openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages
        )
        return response.choices[0].message.content