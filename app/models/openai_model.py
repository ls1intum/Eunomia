import logging
from typing import Any, List

from openai import OpenAI

from app.models.base_model import BaseModelClient


class OpenAIModel(BaseModelClient):
    api_key: str
    _client: OpenAI

    def model_post_init(self, __context: Any) -> None:
        self._client = OpenAI(api_key=self.api_key)
        self.init_model()

    def complete(self, prompt: list) -> str:
        response = self._client.chat.completions.create(
            messages=prompt,
            model=self.model,
        )
        # logging.info(f"Got prompt: {prompt}")
        logging.info(f"Got response for model {self.model}: {response}")
        # confidence = float(response['logprobs']['content']) if response.get('logprobs') and response['logprobs'].get(
        #     'content') is not None else 0.81
        return response.choices[0].message.content

    def init_model(self) -> None:
        logging.info("Skipping init_model due to different expected input type")
        #self.complete(["HI"])
