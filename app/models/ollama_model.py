import json
import logging
from dataclasses import field
from typing import Literal, Any
from openai import OpenAI

from app.prompts.classification_prompt import generate_classification_prompt


class OllamaModel:
    type: Literal["ollama"]
    model: str
    url: str
    _client: OpenAI

    def __init__(self, url: str, model: str, api_key: str):
        logging.info("Initializing OllamaModel")
        self.url = url
        self.model = model
        self._client = OpenAI(base_url=self.url, api_key=api_key)

    def complete(self, email_text: str, subject: str) -> json:
        messages = generate_classification_prompt(body=email_text, subject=subject)
        response = self._client.chat.completions.create(
            messages=messages,
            model=self.model
        )

        logging.info(f"Got prompt, {messages}")
        logging.info(f"Got the response for: {self.model}, {response}")
        return response.choices[0]["message"]["content"]
        # data = {}
        # data['classification'] = 'non-sensitive'
        # data['confidence'] = '50%'
        # logging.info("Completed")
        # return data

