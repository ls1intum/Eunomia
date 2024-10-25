from app.common.environment import config
from app.models.base_model import BaseModelClient
from app.models.ollama_model import OllamaModel
from app.models.openai_model import OpenAIModel

default_model_name = "llama3.1:70b"


def get_model_client() -> BaseModelClient:
    use_openai = config.USE_OPENAI.lower() == "true"
    if use_openai:
        if not config.API_KEY:
            raise ValueError("OpenAI API key must be provided when use_openai is True")
        return OpenAIModel(model=config.OPENAI_MODEL, api_key=config.API_KEY, url=config.OPENAI_API_URL)
    else:
        return OllamaModel(model=config.OLLAMA_MODEL, url=config.OLLAMA_URL)
