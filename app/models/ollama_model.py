import logging
from typing import Dict, Optional

import requests
from pydantic import ConfigDict

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
    url: str
    headers: Optional[Dict[str, str]] = None
    session: requests.Session = requests.Session()

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def model_post_init(self, **kwargs):
        logging.info("Initializing OllamaModel")
        self.headers = create_auth_header()
        self.init_model()

    def complete(self, prompt: []) -> (str, float):
        response = self.session.post(
            f"{self.url}chat",
            json={"model": self.model, "messages": prompt, "stream": False,
                  "options": {"logprobs": True, "temperature": 0.3}},
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
        if self.session:
            self.session.close()

    def init_model(self):
        logging.info("Initializing Ollama model")
        self.complete(["Hi"])
