import json
import logging
import os
from enum import Enum
from typing import Literal, Optional, Dict, Any

import requests
from pydantic import BaseModel, Field, PositiveInt
from openai import OpenAI
from transformers import LlamaModel

from app.prompts.classification_prompt import generate_classification_prompt


class BaseModelClient:
    def __init__(self, model: str):
        self.model = model

    def complete(self, email_text: str, subject: str) -> (str, float):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def generate_prompt(self, email_text: str, subject: str) -> Any:
        return generate_classification_prompt(body=email_text, subject=subject)


class OpenAIModel(BaseModelClient):
    def __init__(self, model: str, api_key: str):
        super().__init__(model)
        logging.info("Initializing OpenAIModel")
        self._client = OpenAI(api_key=api_key)

    def complete(self, email_text: str, subject: str) -> (str, float):
        messages = self.generate_prompt(email_text, subject)
        response = self._client.chat.completions.create(
            messages=messages,
            model=self.model,
            logprobs=True
        )
        logging.info(f"Got prompt: {messages}")
        logging.info(f"Got response for model {self.model}: {response}")
        confidence = float(response['logprobs']['content']) if response.get('logprobs') and response['logprobs'].get('content') is not None else 0.81
        return response.choices[0]["message"]["content"], confidence


def create_auth_header() -> Dict[str, str]:
    gpu_user = os.getenv("GPU_USER")
    gpu_password = os.getenv("GPU_PASSWORD")
    if gpu_user and gpu_password:
        return {
            'Authorization': requests.auth._basic_auth_str(gpu_user, gpu_password)
        }
    return {}


class OllamaModel(BaseModelClient):
    def __init__(self, model: str, url: str):
        super().__init__(model)
        logging.info("Initializing OllamaModel")
        self.url = url
        self.headers = create_auth_header()

    def complete(self, email_text: str, subject: str) -> (str, float):
        messages = self.generate_prompt(email_text, subject)
        response = requests.post(
            f"{self.url}chat",
            json={"model": self.model, "messages": messages, "stream": False,
                  "options": {"logprobs": True, "temperature": 0.7}},
            headers=self.headers
        )
        response.raise_for_status()
        response_data = response.json()
        logging.info(f"Got prompt: {messages}")
        logging.info(f"Got response for model {self.model}: {response_data}")
        confidence = float(response_data['logprobs']['content']) if response_data.get('logprobs') and response_data['logprobs'].get('content') is not None else 0.81
        return response_data["message"]["content"], confidence


default_model_name = "llama3.1:70b"


def get_model_client(use_openai: bool, openai_api_key: str, model_uri: str, model_name: str = "llama3.1:70b") -> BaseModelClient:
    if use_openai:
        if not openai_api_key:
            raise ValueError("OpenAI API key must be provided when use_openai is True")
        return OpenAIModel(model=model_name, api_key=openai_api_key)
    else:
        return OllamaModel(model_name, model_uri)
