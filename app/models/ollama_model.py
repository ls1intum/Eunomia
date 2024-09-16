import logging
from typing import Dict

import requests

from app.common.environment import config
from app.models.base_model import BaseModelClient


def create_auth_header() -> Dict[str, str]:
    gpu_user = config.GPU_USER
    gpu_password = config.GPU_PASSWORD
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
        self.init_session()
        self.init_model()

    def init_session(self):
        self.session = requests.Session()

    def complete(self, prompt: []) -> (str, float):
        response = self.session.post(
            f"{self.url}chat",
            json={"model": self.model, "messages": prompt, "stream": False,
                  "options": {"logprobs": True, "temperature": 0.5}},
            headers=self.headers
        )
        response_data = response.json()
        logging.info(f"Got response for model {self.model}: {response_data}")
        response.raise_for_status()
        logging.info(f"Got prompt: {prompt}")
        confidence = float(response_data['logprobs']['content']) if response_data.get('logprobs') and response_data[
            'logprobs'].get('content') is not None else 0.81
        return response_data["message"]["content"], confidence

    def close_session(self):
        # Close the session when done
        if self.session:
            self.session.close()

    def init_model(self):
        logging.info("Initializing Ollama model")
        response = self.session.get(
            f"{self.url}tags",
            headers=self.headers
        )
        response.raise_for_status()
