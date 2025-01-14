import logging
from typing import Any

from openai import OpenAI

from app.models.base_model import BaseModelClient


class OpenAIBaseModel(BaseModelClient):
    api_key: str
    _client: OpenAI

    def __init__(self, client: Any, model: str, temperature: float = 0.3):
        self._client = client
        self.model = model
        self.temperature = temperature

    def complete(self, prompt: list) -> str:
        response = self._client.chat.completions.create(
            messages=prompt,
            model=self.model,
            temperature=self.temperature
        )
        logging.info(f"Got response for model {self.model}: {response}")
        # confidence = float(response['logprobs']['content']) if response.get('logprobs') and response['logprobs'].get(
        #     'content') is not None else 0.81
        return response.choices[0].message.content
