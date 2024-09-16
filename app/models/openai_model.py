import logging

from openai import OpenAI

from app.models.base_model import BaseModelClient


class OpenAIModel(BaseModelClient):
    def __init__(self, model: str, api_key: str, url: str):
        super().__init__(model)
        logging.info("Initializing OpenAIModel")
        self.url = url
        self.model = model
        self._client = OpenAI(base_url=self.url, api_key=api_key)

    def complete(self, prompt: []) -> (str, float):
        response = self._client.chat.completions.create(
            messages=prompt,
            model=self.model,
            logprobs=True
        )
        logging.info(f"Got prompt: {prompt}")
        logging.info(f"Got response for model {self.model}: {response}")
        confidence = float(response['logprobs']['content']) if response.get('logprobs') and response['logprobs'].get('content') is not None else 0.81
        return response.choices[0]["message"]["content"], confidence
